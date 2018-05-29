2D tomography simulation using radon transform and reconstruction with summary method (backpropagation).


# Usage

+ Prepare square image in greyscale
+ Run script `python gui.py`
+ Configure simulation
+ Click *scan* button to start simulation
+ Wait until processing is done (progress will be displayed in command line)

# Configuration

| param | description |
| :---: | :---------: |
| path | path to input image |
| resolution | number of detectors |
| sampling | how many different angles should be scanned |
| span | radiation cone angular span in radians (usually 3.141 should be fine) |
| filter | if checked ramp filter will be applied to sinogram before reconstruction |

# Screenshot

<img src="https://github.com/buyuk-dev/tomography-2D/blob/master/screenshot.png" alt="screenshot" width="400">

