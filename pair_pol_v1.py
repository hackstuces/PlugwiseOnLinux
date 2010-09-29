from CrcMoose import *
import serial
import getopt, sys, os
import struct, math
from time import sleep

class Plugwise:
    def __init__(self, port, macaddressidentity,macaddress):
        self.serial = serial.Serial(port, "115200")
        self.HEADER = '\x05\x05\x03\x03'
        self.ENDLINE = '\x0d\x0a'
        self.RESPONSEMac = '0019'
        self.RESPONSEVar = '00'
	self.RESPONSEStick = '00'
	self.RESPONSEMaster = '00'
        self.macaddressidentity = macaddressidentity
        self.macaddress = macaddress

    def InitialisationCirclePlus(self):
	time = ['0','1']
        for x in time :
		if x == '0':
        		self.SendCommandInit("0001CAAB")
        		self.GetResult(self.RESPONSEStick)
			self.SendCommandInit("000AB43C")
			self.SendCommand("000400010000000000000000" + self.macaddressidentity)
			self.GetResult(self.RESPONSEMaster)
			print "Linking to Circle+..."
			sleep(35)
	        if x == '1':
			self.SendCommand("000401010000000000000000" + self.macaddressidentity)
        	        self.GetResult(self.RESPONSEMaster)
			self.SendCommand("0023"+ self.macaddressidentity)
			self.GetResult(self.RESPONSEVar)
			print "Connected to Circle+" 

    def InitialisationCircle(self):
        self.SendCommandInit("0008014068")
        self.GetResult(self.RESPONSEVar)

    def PairCircle(self):
        self.SendCommand("000701" + self.macaddressidentity)
        self.GetResult(self.RESPONSEVar)
        self.SendCommand("0023"+ self.macaddressidentity)
        self.GetResult(self.RESPONSEVar)

    def NetworkInfo(self):
        i = ['00','01','02','03','04','05','06','07','08','09','0A','0B','0C','0D','0E','0F','10','11','12','13','14','15','16','17','18','19','1A','1B','1C','1D','1E','1F','20','21','22','23','24','25','26','27','28','29','2A','2B','2C','2D','2E','2F','30','31','32','33','34','35','36','37','38','39','3A','3B','3C','3D','3E','3F']
	prise = ''
        for x in i :
          self.SendCommand("0018" + "000D6F00003" + macaddress + x)
          result = self.GetResult(self.RESPONSEMac)
          var = result[11]+result[12]+result[13]+result[14]+result[15]
	  if var == self.macaddress:
		prise = 1
        if prise == 1:
		return 0
	else:
		return 1

    def GetCRC16(self, value):
        value = CRC16X.calcString(value)
        format = ("%%0%dX" % ((CRC16X.width + 3) // 4))
        return format % value

    def SendCommandInit(self, command):
        self.serial.write(self.HEADER + command + \ self.ENDLINE)

    def SendCommand(self, command):
        self.serial.write(self.HEADER + command + self.GetCRC16(command) + \ self.ENDLINE)

    def GetResult(self, responsecode):
        readbytes = 0

        if responsecode == self.RESPONSEMac:
            readbytes = 38
	elif responsecode == self.RESPONSEStick:
	    readbytes = 100  
	elif responsecode == self.RESPONSEMaster:
	    readbytes = 100
        elif responsecode == self.RESPONSEVar:
            readbytes = 190
        elif responsecode == "0000":
            readbytes = 0

        data = ''

        while 1:
            data += self.serial.read(1)
            if data.endswith(responsecode):
                data = self.serial.read(readbytes)
                return data[16:]

def main():
    print "**************************************************************"
    print "*                          Menu :                            *"
    print "*                                                            *"
    print "*  m  : Pair your Circle+ (Master) with USB stick            *"
    print "*  s  : Pair your Circle (Slave) with Circle+                *"
    print "*  q  : Exit                                                 *"
    print "*                                                            *"
    print "**************************************************************"
    print
    print "Enter a letter from the menu above :"
    arg = raw_input()
    print

    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:s:q:",
                     ['master', 'slave', 'quit'])
    except getopt.error, why:
        print_help()

    port = 16
    macaddressidentity = ''
    macaddress = ''
    command = ''

    if arg == "m":
	   print
	   print "Installation Circle+"
	   print "Step 1 :"
	   print "Enter the path of your usb stick, for example : /dev/ttyUSB0 :"
	   port = raw_input()
	   print "Step 2 :"
	   print "Enter the macaddress address of your Circle+ :"
	   macaddress = raw_input()
	   macaddressidentity = "000D6F00003" + macaddress
	   command = "MASTER"
    elif arg == "i":
	   print 
	   print "Installation Circle"
	   print "Step 1 :"
	   print "Enter the path of your usb stick, for example : /dev/ttyUSB0 :"
	   port = raw_input()
	   print "Step 2 :"
	   print "Enter the macaddress address of your Circle :"
	   macaddress = raw_input()
	   macaddressidentity = "000D6F00003" + macaddress
	   command = "SLAVE"
    elif arg == "q":
	   sys.exit(0)
    else : 
	   print "Command Error ! Select only one letter below !"
	   main()


    plugwise = Plugwise(port, macaddressidentity, macaddress)


    if command == "SLAVE":
	    print
            print "Installation..."
            plugwise.InitialisationCircle()
	    print "Initialisation..."
	    print "Linking to your Circle..."
            plugwise.PairCircle()
	    print "Checking network..."
            plugwise.NetworkInfo()
            while plugwise.NetworkInfo() == 1:
                 plugwise.InitialisationCircle()
                 plugwise.PairCircle()
                 plugwise.NetworkInfo()
	    print "Your plug has been paired to the network successfully"
	    print
            main()
    elif command == "MASTER":
	    print 
            print "Installation..."
	    print "Initialisation Circle+..."
	    plugwise.InitialisationCirclePlus()
	    print
            main()

def init():
    print
    print
    print "**************************************************************"
    print "*                                                            *"
    print "*                 Pair Plugwise On Linux                     *"
    print "*              http://hackstuces.blogspot.com                *"
    print "*              contact : hackstuces@gmail.com                *"
    print "*                                                            *"
    print "**************************************************************"
	
init()
main()


