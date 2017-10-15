
# Rigol VXI11 remote control tool for the command line

## Tools

Remote-control via all interfaces supported by VXI11 interface.

Supported features:

* save screenshot.

* save recorded waveforms from memory. data for each channel is saved as string of unsigned chars. supports saving multiple records and all visible channels.

* save and restore current setup. (some settings sadly cannot be saved, like channel labels)

## Dependencies

### python-vxi11

basic python interface to vxi11

https://github.com/python-ivi/python-vxi11

## Prior Art

### scopeio

Small utility to get screen dumps and measured data from Rigol DS1054 oscilloscope, using vxi11 software transport over Ethernet

https://github.com/LuhaSoft/scopeio

### PyDSA

Spectrum Analyzer for the Rigol DS1000 series digital scopes

https://github.com/rheslip/PyDSA

