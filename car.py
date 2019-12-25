import os, csv, time, serial, threading
from flask import (Flask, Blueprint, request)
from datetime import datetime
from scapy.all import *

from . import db
from .Sensor.GY955 import GY955
from .Module import motor
from .Module import beacon

# file path to save beacon information
t = datetime.now().strftime('%Y_%m_%d_%H:%M:%S')

dirPath = os.path.dirname(os.path.abspath(__file__)) + '/Data'
if not os.path.isdir(dirPath):
    os.mkdir(dirPath)
    
beaconPath = dirPath + '/BeaconInfo_' + t + '.csv' 

# default monitor interface
iface = 'wlan1'

# object of beacon information class
beacon = beacon.Beacon(iface, beaconPath)

# object of car direction class
motor = motor.Direction()

# object of GY955 class
ser = serial.Serial('/dev/ttyAMA0', 9600)
GYdata = GY955(ser)

# initial Euler data
initEuler = None

# object of current app
app = None

# control thread work
adjustRun = False
hopperRun = False
beaconRun = False

# get current app in "__init__.py"
def CurrentApp(currApp):
    global app
    app = currApp

# adjust car bias
def Adjust():
    global adjustRun
    global motor
    global GYdata
    global initEuler
    
    adjustRun = True
    print("start adjusting direction")
    while adjustRun:
        currEuler = GYdata.Euler()
        yaw = currEuler['Yaw'] - initEuler['Yaw']
        motor.Adjust(yaw)
        time.sleep(0.5)
        
    print("stop adjusting direction")

# hopper Wi-Fi channel
def Hopper():
    global hopperRun
    global beacon
    
    hopperRun = True
    print("start hoppering channel")
    while hopperRun:
        beacon.Hopper()

    print("stop hoppering channel")

# get beacon information of Hopper channel
def Beacon():
    global beaconRun
    global beacon
    global app
    
    beaconRun = True
    print("start collecting beacon information")
    with app.app_context():
        database = db.get_db()
        while beaconRun:
            data = beacon.Sniff()
            database.execute('INSERT INTO Beacon (ssid, bssid, dBm, ntp, channel) VALUES (?, ?, ?, ?, ?)',
            (data[0], data[1], data[2], data[3], data[4]))
            database.commit()
    
    print("stop collecting beacon information")

bp = Blueprint('car', __name__)
# set interface to monitor mode
@bp.route('/iface', methods = ('GET', 'POST'))
def Iface():
    global beacon
    global iface
    global beaconRun
    
    if request.method == 'POST':
        iface = request.form['iface']

    if beaconRun:
        beaconRun = False
        beacon.Iface(iface)
        thread = threading.Thread(target = Beacon)
        thread.start()
    else:
        beacon.Iface(iface)
    
    return '', 204
    
# control car direction
@bp.route('/survey')
def Survey():
    global motor
    global GYdata
    global initEuler
    
    initEuler = GYdata.Euler()
    
    thread1 = threading.Thread(target = Adjust)
    thread1.start()
    
    thread2 = threading.Thread(target = Hopper)
    thread2.start()

    thread3 = threading.Thread(target = Beacon)
    thread3.start()
    
    motor.Dir('F')
    
    return 'survey'

@bp.route('/forward')
def Forward():
    global motor
    motor.Dir('F')
    
    return 'forward'

@bp.route('/back')
def Back():
    global motor
    motor.Dir('B')
    
    return 'back'

@bp.route('/left')
def Left():
    global motor
    motor.Dir('L')
    
    return 'left'

@bp.route('/right')
def Right():
    global motor
    motor.Dir('R')
    
    return 'right'

@bp.route('/stop')
def Stop():
    global motor
    global adjustRun
    global hopperRun
    global beaconRun
    
    motor.Dir('S')
    adjustRun = False
    hopperRun = False
    beaconRun = False
    
    return 'stop'