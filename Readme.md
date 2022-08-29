# Smart Meter Reader

Core idea: Read measurement data from a smart meter and publish it on a sink (at
the moment only [Homie 4.0.0][homie4] is suppoted).

The clients and sinks are running as `asyncio.Task` with their own infinite loop
and put/get the data on a central `asyncio.queue` with a very simple `dict` data
exchange model.

## Configuration

Configuration management is done with [dynaconf] with environments enabled (see
[here][dynaconf_envs]). It is recommended to give every configured meter a
dedicated environment name. In my case:

* `dummy`: Dummy client and sink
* `t210`: Sagemcom T210-D-r electric smart meter with according homie sink
* `kamstrup_403`: Kamstrup 403 heat smart meter with according homie sink

Feel free to add own configurations with own namings.

It is expected to find in the working directory where the package is executed:

* `config.py`
* `settings.toml`
* OPTIONAL: `.secrets.toml`

*Remark*: all secret variables

## Running standalone

If you want to run this packages as standalone executable (using the dummy
client and homie sink):

```shell
export ENV_FOR_DYNACONF="dummy"
poetry python3 -m smart_meter_reader
```

It does not support command line arguments as it is expected to be configured
using [dynaconf].

## Service

In the folder `etc` a systemd unit template file is provided. The argument
identifier in the service instance is used as an identifier for the
configuration environment.

* `smart_meter_reader@t210.service`
* `smart_meter_reader@kamstrup_403.service`

## Hardware

I decided to run the smart-meter-reader on a Raspberry Pi. The reason is that
additional services (in my case [homegear][homegear] is running to connect
homematic devices to [openhab][openhab]) are running on this compute unit.

All communication to the clients is realized via serial communication.

## Clients

### Sagemcom T210-D-r

I am connecting to a Sagemcom T210-D-r as provided by [Energie Steiermark
(Austria)][estmk] via the P1 interface ([specifiction 5.0.2][p1_spec] - [list of
further documents for DSMR][dsmr_docs]).

For interpretation of the encrypted payload [this repo][sage] was the important
key to success - thanks to schopenhauer!

**Interface hardware**: There are multiple options to interface with the P1
interface (Open collector serial output - see [specifiction 5.0.2][p1_spec]). I
decided to build a small prototype hat for the Raspberry Pi following this
[cuircuit design][tasmote_p1_interface]

### Kamstrup Multical 403

I was not able to find any official documentation from Kamstrup on the protocoll
which is ued on the IR interface. Thanks to [golles/ha-kamstrup_403][3] and
[bsdphk/PyKamstrup][4] I was able to set up the communication

**Interface hardware**: There are multiple options for infrared read/write heads
- I am using the one from [Volkszaehler.org][vz_ir_head].

## Credits and Acknowledgements

The whole code is built on top of some great prior work. I mention here
explicitly the less "default" but for this purpose directly relevant
implementations (ordering does not reflect importance ;-) ):

* [schopenhauer/sage][sage]: I would have miserably failed on interpreting the
      encrypted data message from the Sagecom T210-D-r without this work and the
      great explainations
* [ndokter/dsmr_parser][2]: This library is used the PyPi hosted package to
      parse the DSMR telegrams to python objects
* [golles/ha-kamstrup_403][3]: I used directly the source code (because I didn't
      wanted to introduce dependencies to homegear) -> But a big thanks to
      golles for his work!
* [bsdphk/PyKamstrup][4]: I guess this is the origin of the very famous
      "kamstrup.py" file a lot of people are depending on. Thanks bsdphk for
      your work!
* [mjcumming/Homie4][6]: Implementation of the Homie 4.0.0 standard which I used
      to generate the data sink

[dynaconf]: https://www.dynaconf.com/
[2]: https://github.com/ndokter/dsmr_parser
[3]: https://github.com/golles/ha-kamstrup_403
[4]: https://github.com/bsdphk/PyKamstrup
[sage]: https://github.com/schopenhauer/sage
[6]: https://github.com/mjcumming/Homie4
[homegear]: https://homegear.eu/
[openhab]: https://www.openhab.org/
[estmk]: https://www.e-steiermark.com/privat
[p1_spec]: https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_a727fce1f1.pdf
[dsmr_docs]: https://www.netbeheernederland.nl/dossiers/slimme-meter-15/documenten
[tasmota_p1_interface]: https://tasmota.github.io/docs/P1-Smart-Meter/
[vz_ir_head]: https://wiki.volkszaehler.org/hardware/controllers/ir-schreib-lesekopf-usb-ausgang
[dynaconf_envs]: https://www.dynaconf.com/configuration/#environments
[homie4]: https://homieiot.github.io/specification/spec-core-v4_0_0/
