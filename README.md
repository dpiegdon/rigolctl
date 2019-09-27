
# Rigol VXI11 remote control tool for the command line

## Tools

Remote-control via all interfaces supported by VXI11 interface.

Supported features:

* save screenshot.

* save recorded waveforms from memory. data for each channel is saved as string of unsigned chars. supports saving multiple records and all visible channels.

* save and restore current setup. (some settings sadly cannot be saved, like channel labels)

* scripts to convert dumped channel data to wave and sigrok format, thus making downloaded data analyzable in e.g. pulseview

## Extra devices

In lack of a better place I also keep my other screenshot scripts here.
Those are for real GPIB device (IEEE 488) from other vendors that I have:

 * HP 53310a Modulation Domain Analyzer
 * LeCroy LC574AL Ocsilloscope

## Dependencies

### python-vxi11

basic python interface to vxi11

https://github.com/python-ivi/python-vxi11

### other GPIB devices

To use the other GPIB screenshot tools, you will need the linux-gpib tools and a GPIB adapter.

## Prior Art

### scopeio

Small utility to get screen dumps and measured data from Rigol DS1054 oscilloscope, using vxi11 software transport over Ethernet

https://github.com/LuhaSoft/scopeio

### PyDSA

Spectrum Analyzer for the Rigol DS1000 series digital scopes

https://github.com/rheslip/PyDSA

