# Hardware

- Raspberry Pi
- breadboard
- [cables](https://dratek.cz/arduino/1214-eses-40-x-f-m-dupont-kabel.html) (kabely na propojení na breadboardu a breadboard mám)
- [soil humidity sensor](https://dratek.cz/arduino/1399-eses-pudni-vlhkomer-pro-jednodeskove-pocitace.html)
- [water pump](https://dratek.cz/arduino/1271-eses-mini-cerpadlo.html)
- [water level sensor](https://dratek.cz/arduino/1160-plovakovy-senzor-vodni-hladiny.html)
- [relay](https://dratek.cz/arduino/886-arduino-rele-5v-1-kanal.html)

## Soil humidity

Soil humidity sensor gives us an analog signal, which is convert to digital and
then received by the Raspberry Pi using the SPI protocol.

- [Raspberry pi SPI wiring](https://pinout.xyz/pinout/spi#)
- [Helpful tutorial](https://tutorials-raspberrypi.com/measuring-soil-moisture-with-raspberry-pi/)
- [Python SPI library](https://github.com/doceme/py-spidev)
