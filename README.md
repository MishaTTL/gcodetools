gcodetools - Hacklab.to Version
==========

CAM extension for Inkscape to export paths to Gcode. Modified to upload directly to Hacklab.to Laser Cutter.

More info at http://www.cnc-club.ru/forum/viewtopic.php?t=35

Use
==========

This works exactly like the original gcodetools, except after generating the .ngc file it uploads it to the Laser Cutter and starts cutting immediately. To use, make sure the laser controller is turned on, AXIS is open, and both computers are connected to the local area network. Click "Path to Gcode" as usual, and the commands will be sent to the Laser Cutter immediately. Warning, the error handling is not robust so save your work before converting!



License
==========
Inkscape and Gcodetools are licensed under GNU GPL.



Install
==========

New to this version:

To use this modified version, install paramiko and scp 0.10.2 (scp module for paramiko).

pip install paramiko
pip install scp

Also, due to some issue on the Linuxcnc, the laser thinks it is not homed even when it is. To use this modified version of gcodetools, start up AXIS software with a modified INI config file in Misha's folder. This ignores the homing constraint so be careful!

Windows

Unpack and copy all the files to the following directory Program Files\Inkscape\share\extensions\ and restart inkscape.

Execute python create_inx.py to create all inx-files.

Linux

Unpack and copy all the files to the following directory /usr/share/inkscape/extensions/ and restart inkscape.

Execute python create_inx.py to create all inx-files.
