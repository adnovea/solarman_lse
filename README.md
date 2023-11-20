# Solarman integration for Ethernet LSE Stick Logger
Home Assistant component for interacting with Solarman LSE (_Ethernet type_) Stick loggers. 

> [!NOTE]
> BEFORE considering using this add-on :
> 
> if you have a **LSW (wifi) Stick Logger**, this add-on won't work. Please use [home_assistant_solarman](https://github.com/StephanJoubert/home_assistant_solarman)
>
> if you have a **LSE (Ethernet) Stick Logger**, you better try first the [Sunsynk](https://github.com/kellerza/sunsynk) Add-on.  

## Foreword
I tried the **Sunsynk add-on**, but I encountered long pauses (*10-30 mins*) in the data recovery that made the add-on useless.
I created a MODS of the old **home_assistant_solarman** add-on version to support the LSE Stick loggers, but unfortunately, the new version is based on the SolarmanV5 lib and not easy to modify (*I'm not a Python developer,  just a handyman*). I decided to "fork" the excellent home_assistant_solarman project to fit my needs and share it on Github.

The scope is not to maintain a Nth Add-on version but only to share my solution.

This code was developed on a **Deye Sun 5K SG03LP1** but could run with other inverters such as SunSynk ones.
> [!CAUTION]
> 
> DISCLAIMER: Use at your own and sole risks! Especially when writing any inverter's registers.

## Installation
Please refer to the [**manual installation**](/custom_components/solarman_lse/README.md) instructions.

Sorry, HACKS is not supported.

## Integration
Solarman LSE uses the same sensors suffix as Home Assistant Solarman, and works well with the nice [Sunsynk-Power-Flow-Card](https://github.com/slipx06/sunsynk-power-flow-card) below:

![image](/docs/images/sunsynk-power-card.jpg)

You can create your own Card with commands for controlling your inverter (*be careful when writing settings because this can irrevocably damage your inverter*).

Each command is sent to the invert BUT the corresponding entities will be updated only at the next read (every +/- 1 minute!!!). Don't repeat the command before at least 1 minute.

*Here is a Card example for my Deye (create your):*
- Time of use on/off (*aka Scheduling*)
- Priority Load or Battery
- Battery Grid Charge enabling (*should be enabled to allow grid charge by time slot*)
- Battery Grid Charge per time slots
- Battery SOC minimum per time slots
- or write automation scripts
- etc.

![image](/docs/images/schedule.jpg)


## DEYE Sun 5K
For the Deye Sun 5K inverter owners, you have to:
- Install the Solarman LSE Add-on
- Copy the *deye.yaml* file under */config/packages*
- Using Hacks, install the *Sunsynk-Power-Flow-Card* add-on.
- Create a Card for the *Sunsynk-Power-Flow-Card* with the sensors
- Create buttons to control the inverter.

## Troubleshooting
- **There is no add-on logo** but the default icon (sorry).
- **Some sensors (or all sensors) show unavailable**. In order to avoid erratic data, I setup some INVALIDATE min/max in the Deye inverter definition file. For example, the Total Solar Production cannot be 0 ! BUT when you start for the 1st time or after a inverter reset, the value may be zero and invalidate all or some sensors. If you have problems, comment all the Invalidate field (and min/max value) and full restart H.A.
- **Sensor display numeric values instead of state**. I have chosen to "interprete" the state within the Cards rather than using the LOOKUP feature in the inverter definition file. It's up to you to re-enable it or create LOOKUP if you need.
- **Commands does not work**. Did you wait a minute at least after the command? Check the logs (*Parameters > System > Logs*). Go to the Solarman_LSE integration and enable debugging, send commands and check the logs. You can also issue direct commands (*Development Tools > Service then search Solarman LSE service*). There are 2 service Simgle and Multiple write. Use single register write to limit the risk and double-check the register address and value for your specific inverter.

