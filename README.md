# Solarman integration for Ethernet LSE Stick Logger
Home Assistant component for interacting with Solarman LSE (_Ethernet type_) Stick loggers. 

> [!NOTE]
> BEFORE considering using this add-on :
> 
> if you have a **LSW (wifi) Stick Logger**, this add-on won't work. Please use [home_assistant_solarman](https://github.com/StephanJoubert/home_assistant_solarman)
>
> if you have a **LSE (Ethernet) Stick Logger** and a Deye or Sunsynk inverter, you better try first the [Sunsynk](https://github.com/kellerza/sunsynk) add-on.  

## Foreword
I tried the **Sunsynk add-on**, but I encountered long pauses (*10-30 mins*) in the data recovery that made the add-on useless.
I created a MODS of the old **home_assistant_solarman** add-on version to support the LSE Stick loggers, but unfortunately, the new version is based on the SolarmanV5 lib and not easy to modify (*I'm not a Python developer,  just a handyman*). I decided to "fork" the excellent home_assistant_solarman project to fit my needs and share it on Github.

The scope is not to maintain a Nth Add-on version but only to share my solution.

This code was developed on a **Deye Sun 5K SG03LP1** but could run with other inverters such as SunSynk ones.
> [!CAUTION]
> 
> **DISCLAIMER**: Use at **your own and sole risks!** Especially when writing any inverter's registers.

## Installation
Please refer to the [**manual installation**](/custom_components/solarman_lse/README.md) instructions.

Sorry, HACKS is not supported.

## Integration
Solarman LSE uses the same sensors suffix as Home Assistant Solarman, and works well with the nice [Sunsynk-Power-Flow-Card](https://github.com/slipx06/sunsynk-power-flow-card) below:

![image](/docs/images/sunsynk-power-card.jpg)

You can create your own Card with commands for controlling your inverter (*be careful when writing settings because this can irrevocably damage your inverter*).

Each command is sent to the invert BUT the corresponding entities will be updated only at the next read (every +/- 1 minute!!!). Don't repeat the command before at least 1 minute.

*Here is a Card example for my Deye (create your):*
- Time of use on/off *aka Scheduling* (*switch.LSE_time_of_use*)
- Priority Load or Battery  (*switch.LSE_priority_mode*)
- Battery Grid Charge enabling (*should be enabled to allow grid charge by time slot*) (*switch.LSE__battery_grid_charge*)
- Battery Grid Charge per time slots  (*switch.LSE_mode_grid_point_1 to 6*)
- Battery SOC minimum per time slots  (*number.LSE_mode_soc_point_1 to 6*)
- or write your own automation scripts  
- etc.

![image](/docs/images/schedule.jpg)


## DEYE Sun 5K
For the Deye Sun 5K inverter owners, you have to:
- Install the Solarman LSE Add-on
- Configure your inverter (*Parameters > Devices & Services > Solarman LSE*). Select the "*deye_sg03lp1_eu.yaml*" file. This file is very detailled and has some limitations to avoid wrong data. This could prevent to see the sensors at startup (*see Toubleshooting section below*)
- Copy the *deye.yaml* file under */config/packages*. This file exposes several additional sensors that you will or not need. Remove the ones unused and create yours using this basis if you need.
- Using Hacks, install the *Sunsynk-Power-Flow-Card* add-on.
- Create a Card for the *Sunsynk-Power-Flow-Card* with the correponding sensors
- Create buttons to control the inverter (*see the Integration section above for the Switch and Number sensors*).

My Deye Sun 5K sensors for *Sunsynk-Power-Flow-Card* add-on:
```
entities:
  use_timer_248: switch.LSE_time_of_use
  priority_load_243: switch.LSE_priority_mode
  inverter_voltage_154: sensor.sensor.LSE_grid_voltage_l1
  load_frequency_192: sensor.LSE_load_frequency
  inverter_current_164: sensor.LSE_current_l1
  inverter_power_175: sensor.LSE_inverter_l1_power
  grid_connected_status_194: sensor.LSE_grid_connected_status
  inverter_status_59: sensor.LSE_running_status
  day_battery_charge_70: sensor.LSE_daily_battery_charge
  day_battery_discharge_71: sensor.LSE_daily_battery_discharge
  battery_voltage_183: sensor.LSE_battery_voltage
  battery_soc_184: sensor.LSE_battery_soc
  battery_power_190: sensor.LSE_battery_power
  battery_current_191: sensor.LSE_battery_current
  grid_power_169: sensor.LSE_internal_ct_l1_power
  day_grid_import_76: sensor.LSE_daily_energy_bought
  day_grid_export_77: sensor.LSE_daily_energy_sold
  grid_ct_power_172: sensor.LSE_external_ct_l1_power
  day_load_energy_84: sensor.LSE_daily_load_consumption
  essential_power: sensor.LSE_load_l1_backup_power
  essential_load1: none
  essential_load2: none
  nonessential_power: sensor.LSE_load_l1_home_power
  non_essential_load1: none
  non_essential_load2: none
  aux_power_166: sensor.LSE_gen_power
  aux_load1: none
  aux_load2: none
  aux_connected_status: sensor.LSE_aux_connected_status
  day_aux_energy: none
  day_pv_energy_108: sensor.LSE_daily_production
  pv1_power_186: sensor.LSE_pv1_power
  pv2_power_187: sensor.LSE_pv2_power
  pv3_power_188: none
  pv4_power_189: none
  pv_total: null
  pv1_voltage_109: sensor.LSE_pv1_voltage
  pv1_current_110: sensor.LSE_pv1_current
  pv2_voltage_111: sensor.LSE_pv2_voltage
  pv2_current_112: sensor.LSE_pv2_current
  pv3_voltage_113: none
  pv3_current_114: none
  pv4_voltage_115: none
  pv4_current_116: none
  remaining_solar: none
  battery_temp_182: sensor.LSE_battery_temperature
  radiator_temp_91: sensor.LSE_ac_temperature
  dc_transformer_temp_90: sensor.LSE_dc_temperature
  prog1_time: sensor.LSE_mode_point_1
  prog1_capacity: sensor.LSE_mode_soc_point_1
  prog1_charge: sensor.LSE_mode_grid_point_1
  prog2_time: sensor.LSE_mode_point_2
  prog2_capacity: sensor.LSE_mode_soc_point_2
  prog2_charge: sensor.LSE_mode_grid_point_2
  prog3_time: sensor.LSE_mode_point_3
  prog3_capacity: sensor.LSE_mode_soc_point_3
  prog3_charge: sensor.LSE_mode_grid_point_3
  prog4_time: sensor.LSE_mode_point_4
  prog4_capacity: sensor.LSE_mode_soc_point_4
  prog4_charge: sensor.LSE_mode_grid_point_4
  prog5_time: sensor.LSE_mode_point_5
  prog5_capacity: sensor.LSE_mode_soc_point_5
  prog5_charge: sensor.LSE_mode_grid_point_5
  prog6_time: sensor.LSE_mode_point_6
  prog6_capacity: sensor.LSE_mode_soc_point_6
  prog6_charge: select.LSE_mode_grid_point_6
  energy_cost_buy: none
  energy_cost_sell: none
  solar_sell_247: sensor.LSE_energy_selling
```

## Troubleshooting
- **There is no add-on logo** but the default icon (sorry).
- **Some sensors (or all sensors) show unavailable**. In order to avoid erratic data, I setup some INVALIDATE min/max in the Deye inverter definition file. For example, the Total Solar Production cannot be 0 ! BUT when you start for the 1st time or after a inverter reset, the value may be zero and invalidate all or some sensors. If you have problems, comment all the Invalidate field (and min/max value) and full restart H.A.
- **Sensor display numeric values instead of state**. I have chosen to "interprete" the state within the Cards rather than using the LOOKUP feature in the inverter definition file. It's up to you to re-enable it or create LOOKUP if you need.
- **Commands does not work**. Did you wait a minute at least after the command? Check the logs (*Parameters > System > Logs*). Go to the Solarman_LSE integration and enable debugging, send commands and check the logs. You can also issue direct commands (*Development Tools > Service then search Solarman LSE service*). There are 2 service Simgle and Multiple write. Use single register write to limit the risk and double-check the register address and value for your specific inverter.

