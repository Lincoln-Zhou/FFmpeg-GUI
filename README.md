# FFmpeg-GUI

A GUI video processing tool based on FFmpeg

FFmpeg GUI combines the convenience and clarity of GUI with FFmpeg's great capability. This program is developed using Python and PyQt5 GUI framework.

## Sample
<img src="https://github.com/Lang-Zhou/FFmpeg-GUI/blob/master/reserved/Sample.png" width="60%" />
(Test Environment: macOS 10.15.5, Python 3.8.2)

## Dependency & Requirements

### Dependency
* FFmpeg 4.0.5 or later
* PyQt5
* Python 3.4 ~ 3.10 (Currently no tests are done on newer versions)

### System Requirements
* macOS 10.13 High Sierra or later
* Microsoft Windows 7 or later
* Linux (tested on Kali Linux 2020.3 with Python 3.8.5, no guarantee for all distributions)

## Run & Deployment
* To run directly from `.py` file, make sure all `.py` files in `master` branch are in the same folder, and execute `python mainWIndow.py` from terminal.
* In future updates, executable files packaged for macOS, Windows and major Linux distributions might be available.

## Todo List
### Short Term
* A fully functional progressbar
* More codec options for processing audio
* Better file I/O
* Reducing potential contradictions caused by user customized codec parameters

### Long Term
* Integrating muliti-processing to improve program efficiency on multi-core computers
* Hardware acceleration for certain platforms
* More functions
* Optimizing UI for different systems

## Feedbacks
The program is still in its early stage of development and bugs are unavoidable. GitHub issues and E-mails are welcomed to report bugs or give suggestions.

## License
The program is under GNU GPL v3 license. For more license information, refer to LICENSE.md

## Release History
* 2020/06/02 0.1.2
* 2020/05/21 0.1.1
* 2020/05/05 0.1 Alpha
