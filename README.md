# Headless RaspberryPI Partition Manager

Small command line utilitiy based on [PyInvoke](https://www.pyinvoke.org/) to manage a multi partition/OS RaspberryPI board in a headless mode.

Provided that the board has some distros installed with [PINN](https://github.com/procount/pinn), it will allow to mount the paritions in the OS boot screen mode.

Requirements for operation:

* Add `vncinstall forcetrigger ssh` to `recovery.cmdline`
* Create a `wpa_supplicant.conf` in the same partition.
* Boot your Raspberry with the above configuration and find it's IP address.
* Add the environment variables `HOST`, `RPI_USER`, `RPI_PASSWORD`


## Notes
