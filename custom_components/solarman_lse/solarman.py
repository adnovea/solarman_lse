# ----------------------------------------------------------------------
#  Solarman_LSE for LSE-3 Stick Logger
#  Use Raw Modbus RTU protocol w/o Solarman V5 encapsulation
#
#  AdNovea - Nov 2023
# ----------------------------------------------------------------------

import socket
import yaml
import logging
import struct
from homeassistant.util import Throttle
from datetime import datetime
from .parser import ParameterParser
from .const import *


log = logging.getLogger(__name__)


START_LSE             = 0x03
SERIAL_LSE            = 0xE8
PROTOCOL_BYTE         = [0x00, 0x00]
QUERY_RETRY_ATTEMPTS  = 6

# Anti-collision: avoid register read/write collisions
COLLISION_FLAG        = 0


# ----------------------------------------------------------------------
# Solarman_LSE class
# ----------------------------------------------------------------------
class Inverter:


    # Class constructor
    # ----------------------------------------------------------------------
    def __init__( self, path, serial, host, port, mb_slaveid, lookup_file ):
    
        self._serial            = serial
        self.path               = path
        self._host              = host
        self._port              = port
        self._mb_slaveid        = mb_slaveid
        self._current_val       = None
        self.status_connection  = "Disconnected"
        self.status_lastUpdate  = "N/A"
        self.lookup_file        = lookup_file
        if not self.lookup_file or lookup_file == 'parameters.yaml':
            self.lookup_file    = 'deye_hybrid.yaml'

        with open( self.path + self.lookup_file ) as f:
            self.parameter_definition = yaml.full_load( f )


    # Raw Modubus protocol for LSE-3 Stick Logger
    # ----------------------------------------------------------------------
    def connect_to_server( self ):
    
        server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        server.settimeout( 6 )
        server.connect( ( self._host, self._port ) )
        return server


    # Create Modbus handler
    # ----------------------------------------------------------------------
    def modbus( self, data ) :
    
        POLY = 0xA001
        crc  = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                crc = ((crc >> 1) ^ POLY
                if (crc & 0x0001)
                else crc >> 1)
        return crc


    # Increment serial counter for pairing requests and replies
    # ----------------------------------------------------------------------
    def serial_counter( self ) :
        
        global SERIAL_LSE
        if SERIAL_LSE < 0xFF:
            SERIAL_LSE += 1
        else:
            SERIAL_LSE = 0xE8
        return

 
    # ----------------------------------------------------------------------
    # READ holding Register
    # ----------------------------------------------------------------------
    #   -- extended array
    #   03 E8         SERIAL
    #   00 00         PROTOCOL
    #   00 06         PACKET LENGTH
    #   -- request array
    #   01            SLAVE ID 
    #   03            FUNCTION
    #   00 F8         Start register (eg. Time Of Use)
    #   00 01         VALUE (NB Registers)
    #   CRC

    # Create request for Holding Register Read
    # ----------------------------------------------------------------------
    def generate_request( self, start, length, mb_fc ):
    
        
        request_data = bytearray( [self._mb_slaveid, mb_fc] )               # Slave address & Function Code
        request_data.extend( start.to_bytes( 2, 'big' ) )                   # Start register address
        request_data.extend( length.to_bytes( 2, 'big' ) )                  # Number of register to read
        crc = self.modbus( request_data )                                   
        request_data.extend( crc.to_bytes( 2, 'little' ) )                  # CRC
        packet_len = request_data.__len__() - 2                             # Length of request

        self.serial_counter()                                               # Increment modbus packet counter
        packet = []
        packet.extend( bytearray( [START_LSE, SERIAL_LSE] ) )               # Serial
        packet.extend( PROTOCOL_BYTE )                                       # Protocol
        packet.extend( packet_len.to_bytes( 2, "big" ) )                    # Request Length
        packet.extend( request_data )                                        # Request

        del request_data
        return packet


    # Send Read register 
    # ----------------------------------------------------------------------
    def send_request( self, params, start, end, mb_fc, sock ):
    
        result = 0
        length = end - start + 1
        request = self.generate_request( start, length, mb_fc )
        try:
            # log.debug( '[send_request] send data: %s', bytes(request).hex() )
            sock.sendall( bytes( request ) )
            raw_msg = sock.recv( 1024 )
            # log.debug( '[send_request] received data: %s', bytes(raw_msg).hex() )
            
            # log.debug( 'raw_msg[1]= %X, SERIAL_LSE= %X', raw_msg[1], SERIAL_LSE )
            if bytes(raw_msg)[1] == SERIAL_LSE:                              # Check if correct serial
                result = 1
                params.parse( raw_msg, start, length )
            else:
                log.debug( '[send_request] wrong serial: %s', bytes(raw_msg).hex() )                
            del raw_msg
            
        finally:
            del request
        return result


    # ----------------------------------------------------------------------
    # WRITE Multiple registers                        WRITE Single register
    # ----------------------------------------------------------------------
    #   -- extended array                             -- extended array
    #   03 EC         SERIAL                          03 E8         SERIAL
    #   00 00         PROTOCOL                        00 00         PROTOCOL
    #   00 09         PACKET LENGTH                   00 06         PACKET LENGTH
    #   -- request array                              -- business array
    #   01            SLAVE ID                        01            SLAVE ID
    #   10            FUNCTION (16)                   06            FUNCTION (6)
    #   00 F8         Start register                  00 F8         Start register (eg. Time Of Use)
    #   00 01         Nb of registers (N) [1-123]     
    #   02            Number of Bytes (N*2)       
    #   00 FE         Register values (Nx2)           00 FE         Register value 
    #   32 68         CRC                             89 BB         CRC

    # Create Message for Single Holding Register Write
    # ----------------------------------------------------------------------
    def generate_packet( self, start, values, mb_fc ):

        cmd_data = bytearray( [self._mb_slaveid, mb_fc] )                 # Slave address & Function Code
        cmd_data.extend( start.to_bytes( 2, 'big' ) )                     # Start register address
        
        if mb_fc == 0x10:                                                  # Fields for multiple registers
          nbval  = values.__len__()
          length = nbval * 2
          cmd_data.extend( nbval.to_bytes( 2, 'big' ) )                   # Number of registers
          cmd_data.extend( bytearray( [length] ) )                        # Length of values
          
        elif mb_fc != 0x06:
            log.warning(f"Service Call: write_(multiple)_holding_registers: Incorrect Function Code [{mb_fc}]")
            return
              
        for value in values:
            cmd_data.extend( value.to_bytes( 2, 'big' ) )                 # Add register's values
        crc = self.modbus( cmd_data)
        cmd_data.extend( crc.to_bytes( 2, 'little' ) )                    # CRC
        packet_len = cmd_data.__len__() - 2                                # Length of request
        # log.debug( '[cmd_data] = %s', bytes(cmd_data).hex() )

        self.serial_counter()                                               # Increment modbus packet counter
        packet = []
        packet.extend( bytearray( [START_LSE, SERIAL_LSE] ) )              # Serial
        packet.extend( PROTOCOL_BYTE )                                      # Protocol
        packet.extend( packet_len.to_bytes( 2, "big" ) )                   # Packet length
        packet.extend( cmd_data )                                           # Payload (business array)

        del cmd_data
        return packet


    # Single Holding Register Write
    # ----------------------------------------------------------------------
    def write_multiple_register ( self, register, values, mb_fc ):
    
        sock = None
        attempts_left = QUERY_RETRY_ATTEMPTS

        try:
            sock = self.connect_to_server()

            while attempts_left > 0:
                attempts_left -= 1
                result         = 0
                command        = None
                try:
                    command = self.generate_packet( register, values, mb_fc) 
                    log.debug( '[write_request] send data: %s', str( command ) )
                    # log.debug( '[write_request] send data: %s', bytes(command).hex() )
                    sock.sendall( bytes( command ) )
                    raw_msg = sock.recv( 1024 )
                    # log.debug( '[write_request] received data: %s', bytes(raw_msg).hex() )
                    
                    if bytes(raw_msg)[1] == SERIAL_LSE:                   # Check if correct serial
                        del raw_msg
                        del command
                        result = 1
                        break
    
                except ConnectionResetError:
                    log.debug( f"[write_request] failed as client closed stream, trying to re-open." )
                    sock.close()
                    sock = connect_to_server()
                except TimeoutError:
                    log.debug( f"[write_request] failed with timeout" )
                except Exception as e:
                    log.debug( f"[write_request] failed with exception [{type(e).__name__}]" )
                    
                # Successful attempt ?
                if result == 0:
                    log.debug( f"[write_request] failed, [{attempts_left}] retry attempts left" )
                else:
                    log.debug( f"[write_request] succeeded" )
                    self.status_lastUpdate = datetime.now().strftime( "%Y/%m/%d %H:%M:%S" )
                    self.status_connection = "Connected"
                    break
                    
            # All attemps failed
            if result == 0:
                log.warning( f"[write_request] failed!" )

        except Exception as e:
            log.warning( f"[write_request] inverter at {self._host}:{self._port} failed on connection start with exception [{type(e).__name__}]" )
            self.status_connection = "Disconnected"
        finally:
            if sock:
                sock.close()


    # Update inverter sensors
    # ----------------------------------------------------------------------
    @Throttle (MIN_TIME_BETWEEN_UPDATES)
    def update ( self ):
    
        # Anti-collision
        global COLLISION_FLAG
        if COLLISION_FLAG == 1:
            attempts_left = QUERY_RETRY_ATTEMPTS
            while attempts_left > 0:
                attempts_left -= 1
                time.sleep( 1 )
                log.debug( f'Write multiple holding register: collision - [{attempts_left}] retry attempts left' )
                if COLLISION_FLAG == 0:
                    break
        if COLLISION_FLAG == 1:
            log.warning( f"Querying registers [{start} - {end}] failed, aborting on collision." )
            return
              
        # Read registers      
        COLLISION_FLAG = 1
        self.get_statistics()
        COLLISION_FLAG = 0
        return


    # Read pool of register requests
    # ----------------------------------------------------------------------
    def get_statistics( self ):
    
        result   = 1
        params   = ParameterParser( self.parameter_definition )
        requests = self.parameter_definition['requests']
        log.debug( f"Starting to query for [{len(requests)}] ranges..." )

        sock = None
        try:
            sock = self.connect_to_server()

            for request in requests:
                start = request['start']
                end = request['end']
                mb_fc = request['mb_functioncode']
                log.debug(f"Querying [{start} - {end}]...")

                attempts_left = QUERY_RETRY_ATTEMPTS
                while attempts_left > 0:
                    attempts_left -= 1
                    result = 0
                    try:
                        result = self.send_request(params, start, end, mb_fc, sock)
                    except ConnectionResetError:
                        log.debug( f"Querying [{start} - {end}] failed as client closed stream, trying to re-open." )
                        sock.close()
                        sock = connect_to_server()
                    except TimeoutError:
                        log.debug( f"Querying [{start} - {end}] failed with timeout" )
                    except Exception as e:
                        log.debug( f"Querying [{start} - {end}] failed with exception [{type(e).__name__}]" )
                    if result == 0:
                        log.debug( f"Querying [{start} - {end}] failed, [{attempts_left}] retry attempts left" )
                    else:
                        log.debug( f"Querying [{start} - {end}] succeeded" )
                        break
                        
                if result == 0:
                    log.warning( f"Querying registers [{start} - {end}] failed, aborting." )
                    break

            if result == 1:
                log.debug( f"All queries succeeded, exposing updated values." )
                self.status_lastUpdate = datetime.now().strftime( "%Y/%m/%d %H:%M:%S" )
                self.status_connection = "Connected"
                self._current_val = params.get_result()
            else:
                self.status_connection = "Disconnected"
        except Exception as e:
            log.warning( f"Querying inverter at {self._host}:{self._port} failed on connection start with exception [{type(e).__name__}]" )
            self.status_connection = "Disconnected"
        finally:
            if sock:
                sock.close()


    # Get register values
    # ----------------------------------------------------------------------
    def get_current_val (self ):
        return self._current_val


    # Get sensor's list of registers and definitions
    # ----------------------------------------------------------------------
    def get_sensors( self ):
        params = ParameterParser( self.parameter_definition )
        return params.get_sensors ()


    # Service calls for Single Holding Register Write
    # Use Multiple Holding register (0x10) write because Deye sun 5K does not support Single Holding register write (0x06)
    # ----------------------------------------------------------------------
    def service_write_holding_register( self, register, value ):
    
        log.debug( f'Write holding register: [{register}], value : [{value}]' )
        try:
            self.write_multiple_register( register, bytearray( [value] ), 0x10 ) 
        except Exception as e:
            log.warning( f"Write holding register: [{register}], value : [{value}] failed with exception [{type(e).__name__}: {e}]" )

        return


    # Service calls for Multiple Holding Register Write
    # ATTENTION : bugs with 2 or more values 
    # ----------------------------------------------------------------------
    def service_write_multiple_holding_registers( self, register, values ):

        log.debug( f'Write multiple holding register: [{register}], values : [{values}]' )

        # Anti-collision
        global COLLISION_FLAG
        if COLLISION_FLAG == 1:
            attempts_left = QUERY_RETRY_ATTEMPTS
            while attempts_left > 0:
                attempts_left -= 1
                time.sleep( 1 )
                log.debug( f'Write multiple holding register: collision - [{attempts_left}] retry attempts left' )
                if COLLISION_FLAG == 0:
                    break
        if COLLISION_FLAG == 1:
            log.warning( f"'Write multiple holding register: failed, aborting on collision." )
            return
              
        # Write registers      
        COLLISION_FLAG = 1
        try:
            log.warning( f"ATTENTION : Multiple Holding Register Write bugs with 2 or more values" )
            self.write_multiple_register( register, values, 0x10 ) 
        except Exception as e:
            log.warning( f"Service Call: write_multiple_holding_registers: [{register}], values : [{values}] failed with exception [{type(e).__name__}: {e}]" )

        COLLISION_FLAG = 0
        return

