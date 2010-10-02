Pair Plugwise on Linux :

This version pairs your Plugwise Circles and Circle+ on Linux.

For the moment, this version pairs sockets with identity "000D6F00003".
It works on firmwares 2008-03-10 (Circle+) and 2008-08-26 (USB stick).

Cloning :

go to a folder (for example /home/user/hackstuces) and run :
git clone git://github.com/hackstuces/PlugwiseOnLinux.git
cd PlugwiseOnLinux

Configuring :

run the command : 

apt-get install python-serial

Using :

go to the folder PlugwiseOnLinux and run : 

python pair_pol_v1.py


Notes :

The pairing is done only when your sockets are initialized. To initialize, connect your Circle during 3 seconds and then disconnect it during 3 seconds. Repeat it 3 times.

After, run the command : 

stty -F /dev/ttyUSB0 ispeed 115200 ospeed 115200 cs8 -parenb


During the pairing (choose m in the menu), the Circle+ have to turn off (during few seconds) then turn on. 
