#!/bin/bash

# These settings allow a shutdown to be invoked by pulling a GPIO pin LOW (BCM17)
# Once shutdown has completed, a GPIO pin is set Low (BCM18)
echo "dtoverlay=gpio-poweroff,gpiopin=18,active_low=0" >> /boot/config.txt
echo "dtoverlay=gpio-shutdown,gpio_pin=17,active_low=1,gpio_pull=up" >> /boot/config.txt
