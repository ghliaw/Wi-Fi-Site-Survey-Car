import os, time, csv, threading
from datetime import datetime
from scapy.all import *

class Beacon():
    def __init__(self, iface = "wlan1", path = 'BeaconInfo.csv'):
        self.iface = iface
        self.path = path
        self.channel = 0
        self.ssid = ''
        self.bssid = ''
        self.hssid = ''
        self.dBm = ''
        self.time = ''
        
        # monitor mode
        os.system('ifconfig %s down' %self.iface)
        os.system('iwconfig %s mode monitor' %self.iface)
        os.system('ifconfig %s up' %self.iface)
        
        # caption of beacon information
        with open(self.path, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ssid","bssid","dBm","ntp"])
            
    # change interface
    def Iface(self, iface):
        os.system('ifconfig %s down' %self.iface)
        os.system('iwconfig %s mode managed' %self.iface)
        os.system('ifconfig %s up' %self.iface)
        
        self.iface = iface
        os.system('ifconfig %s down' %self.iface)
        os.system('iwconfig %s mode monitor' %self.iface)
        os.system('ifconfig %s up' %self.iface)
        
    # change channel
    def Hopper(self):
        self.channel= (self.channel % 11) + 1 
        os.system('iwconfig %s channel %d' % (self.iface, self.channel))
        time.sleep(0.1)
    
    # beacon information will be collect
    def Info(self, pkt):
        if pkt.haslayer(Dot11Beacon):
                self.ssid = str(pkt.getlayer(Dot11Elt).info)
                self.bssid = str(pkt.getlayer(Dot11FCS).addr2)
                self.hssid = pkt.getlayer(Dot11Elt).info
                self.dBm = str(pkt.getlayer(RadioTap).dBm_AntSignal)
                self.time = datetime.now().strftime('%H:%M:%S')
                
                if self.hssid == '' or pkt.getlayer(Dot11Elt).ID != 0:
                    print ("Hidden Network Detected")
                   
                with open(self.path, 'a') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([self.ssid, self.bssid, self.dBm, self.time, self.channel])
    
    # get beacon information what "Info" function want
    def Sniff(self):
        sniff(iface = self.iface, prn=self.Info, timeout = 4.4)
        data = [self.ssid, self.bssid, self.dBm, self.time, self.channel]
        
        return data