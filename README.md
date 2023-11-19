# Solarman integration for LSE Stick Logger
Home Assistant component for interacting with Solarman LSE (_Ethernet type_) Stick loggers. 

> [!NOTE]
> BEFORE considering using this add-on :
> 
> if you have a **LSW (wifi) Stick Logger**, this add-on won't work. Please use [home_assistant_solarman](https://github.com/StephanJoubert/home_assistant_solarman)
>
> if you have a **LSE (Ethernet) Stick Logger**, You may try first the [Sunsynk](https://github.com/kellerza/sunsynk). 

## Some history
I tried the **Sunsynk add-on**, but I encountered long pauses (*10-30 mins*) in the data recovery that made the add-on useless.
I made a MODS of the old **home_assistant_solarman** add-on version to support the LSE Stick loggers, but unfortunately, the new version is based on the SolarmanV5 lib and is not easy to modify.
I decided to "fork" the excellent home_assistant_solarman project to fit my needs and to share it on Github.

This code was developed on a **Deye Sun 5K SG03LP1** but can run with other inverters too.
> [!IMPORTANT]
> The scope is not to maintain a Nth Add-on version but only to share my solution.
> 
> DISCLAIMER: Use at your own risk! Especially when writing any settings.
> 
