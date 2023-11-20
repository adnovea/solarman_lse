# ----------------------------------------------------------------------
# Solarman_LSE for LSE-3 Stick Logger w/o Solarman V5 encapsulation
# ----------------------------------------------------------------------
from datetime import timedelta

DOMAIN = 'solarman_lse'

DEFAULT_PORT_INVERTER = 8899
DEFAULT_INVERTER_MB_SLAVEID = 1
DEFAULT_LOOKUP_FILE = 'deye_hybrid.yaml'
LOOKUP_FILES = [
    'deye_4mppt.yaml',
    'deye_hybrid.yaml',
    'deye_sg03lp1_eu.yaml',
    'deye_sg04lp3.yaml',
    'deye_string.yaml',
    'sofar_g3hyd.yaml',
    'sofar_hyd3k-6k-es.yaml',
    'sofar_lsw3.yaml',
    'sofar_wifikit.yaml',
    'solis_1p8k-5g.yaml',
    'solis_hybrid.yaml',
    'zcs_azzurro-ktl-v3.yaml',
    'custom_parameters.yaml'
]

DEFAULT_LOOKUP_PROTOCOL = 'Raw_Modbus_RTU'
LOOKUP_PROTOCOL = [
    'Raw_Modbus_RTU'
]

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)

CONF_INVERTER_HOST = 'inverter_host'
CONF_INVERTER_PORT = 'inverter_port'
CONF_INVERTER_MB_SLAVEID = 'inverter_mb_slaveid'
CONF_LOOKUP_FILE = 'lookup_file'
CONF_LOOKUP_PROTOCOL = 'lookup_protocol'

SENSOR_PREFIX = 'LSE'
