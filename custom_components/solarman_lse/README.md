

# Solarman_LSE is a Home Assistant Solarman MODS for LSE-3 Stick logger

This add-on is a fork from the excellent Stephan Joubert [Home Assistant Solarman](https://github.com/StephanJoubert/home_assistant_solarman) add-on.
It supports the **LSE-3** Stick Logger (*Ethernet*) that uses a Raw Modbus RTU protocol. Instead, the LSW Stick logger (*Wifi*) requires a Solarman V5 protocol encapsulation as an additional protection of the data transmission.
Solarman LSE add-on was developed and customized for a **DEYE Sun SG03LP1** inverter but could (probably) runs with other types such as SunSynk inverters.

It is highly recomended to use the "*Samba shar*e" add-on (*you will need to enable advanced mode in your user profile*).


> [!CAUTION]
> 
> **DISCLAIMER**: Use of this Add-on is under **your sole and entire responsibility** (*damages, injures, etc.*)
> 
> You have been warned that Writing inverter registers may definitively damage your inverter.
> 
> There is no claims this Add-on will works neither it has been approved for any kind of uses.
>
> The purpose is to share the work I have done for my Deye inverter and not for the purpose of maintaining a specific add-on.
> 



# Manual Installation

1.  Clone or download the repo, and copy the "*solarman_lse*" folder in "*custom_components*" to the "*custom_components*" folder in home assistant.
    After that, the folder structure should look below:
```
    custom_components
    +-- solarman
    ¦   +-- __init__.py
    ¦   +-- config_flow.py
    ¦   +-- const.py
    ¦   +-- manifest.json
    ¦   +-- parser.py
    ¦   +-- scanner.py
    ¦   +-- sensor.py
    ¦   +-- services.py
    ¦   +-- services.yaml
    ¦   +-- solarman.py
    ¦   +-- string.py
    ¦   +-- inverter_definitions
    ¦       +-- {inverter-definition yaml files}
    ¦   +-- translations
    +-- {other components}
```
2.  **IMPORTANT**: Ensure the __pycache__ folder is empty or clear it.

3.  Full restart Home Assistant and wait until reboot is completed.

4.  Click on the "*Configuration*" tab on the left, then on "*Devices & Services*".
    Select the "*Integrations*" tab on the top of the screen.
    Then click on the "*+ ADD INTEGRATION*" button on the left-hand corner.
    Select the "*solarman LSE*" integration.

5.  Enter the name (*e.g. deye to prefix all inverter's sensors*), the IP address, the port (*8899*), the slave N° (*1*).
    The Raw_Modbus_RTU protocol is selected by default.
    Choose the YAMl file corresponding to your inverter (*e.g. deye_sg03lp1_eu.yaml*).


> [!NOTE]
> If you have a previous *Home Assistant Solarman* installation, first remove all the sensors related to this previous installation (*Parameters > Devices & Services > Entities*).
> 
> You may also have to remove the sensors from *Development tools > Statistics* too, but keep in mind that removing Statistics sensors also clear sensor's history.
> 
> If there are still remaining sensors when installing Solarman LSE, because the name of the sensors are identical, the new ones will be suffixed with "_2".


