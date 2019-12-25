import csv, os, serial
from datetime import datetime

class GY955():
    # initial GY-955 module
    def __init__(self, ser):
        self.ser = ser
        self.ser.write(serial.to_bytes([0xAA, 0x00, 0xAA]))

    # get current time
    def Time(self):
        time = datetime.now().strftime('%H:%M:%S.%f')
        return time

    # get accelerometer
    def Acc(self):
        self.ser.write(serial.to_bytes([0xA5, 0x15, 0xBA]))

        data = self.ser.read(12)
        str = "".join("{:02X}".format(c) for c in data)
    
        acc = int(str[8:12], 16)
        if (str[8] != 'F'):
            acc = acc / 100
        else:
            acc = (65536 - acc) /-100
        accX = acc

        acc = int(str[12:16], 16)
        if (str[12] != 'F'):
            acc = acc / 100
        else:
            acc = (65536 - acc) /-100
        accY = acc
    
        acc = int(str[16:20], 16)
        if (str[16] != 'F'):
            acc = acc / 100
        else:
            acc = (65536 - acc) /-100
        accZ = acc
        
        return {'Acc-X': accX, 'Acc-Y': accY, 'Acc-Z': accZ}
    
    # get gyroscpoe
    def Gyro(self):
        self.ser.write(serial.to_bytes([0xA5, 0x25, 0xCA]))

        data = ser.read(12)
        str = "".join("{:02X}".format(c) for c in data)
    
        gyro = int(str[8:12], 16)
        if (str[8] != 'F'):
            gyro = gyro / 16
        else:
            gyro = (65536 - gyro) /-16
        gyroX = gyro
    
        gyro = int(str[12:16], 16)
        if (str[12] != 'F'):
            gyro = gyro / 16
        else:
            gyro = (65536 - gyro) /-16
        gyroY = gyro
    
        gyro = int(str[16:20], 16)
        if (str[16] != 'F'):
            gyro = gyro / 16
        else:
            gyro = (65536 - gyro) /-16
        gyroZ = gyro

        return {'Gyro-X': gyroX, 'Gyro-Y': gyroY, 'Gyro-Z': gyroZ}

    # get magnetometer
    def Magnet(self):
        self.ser.write(serial.to_bytes([0xA5, 0x35, 0xDA]))

        data = self.ser.read(12)
        str = "".join("{:02X}".format(c) for c in data)
    
        magnet = int(str[8:12], 16)
        if (str[8] != 'F'):
            magnet = magnet / 16
        else:
            magnet = (65536 - magnet) /-16
        magnetX = magnet
    
        magnet = int(str[12:16], 16)
        if (str[12] != 'F'):
            magnet = magnet / 16
        else:
            magnet = (65536 - magnet) /-16
        magnetY = magnet
    
        magnet = int(str[16:20], 16)
        if (str[16] != 'F'):
            magnet = magnet / 16
        else:
            magnet = (65536 - magnet) /-16
        magnetZ = magnet

        return {'Magnet-X': magnetX, 'Magnet-Y': magnetY, 'Magnet-Z': magnetZ}

    # get Euler
    def Euler(self):
        self.ser.write(serial.to_bytes([0xA5, 0x45, 0xEA]))

        data = self.ser.read(12)
        str = "".join("{:02X}".format(c) for c in data)
        
        euler = int(str[8:12], 16)
        if (str[8] != 'F'):
            euler = euler / 100
        else:
            euler = (65536 - euler) /-100
        yaw = euler
        
        euler = int(str[12:16], 16)
        if (str[12] != 'F'):
            euler = euler / 100
        else:
            euler = (65536 - euler) /-100
        roll = euler
        
        euler = int(str[16:20], 16)
        if (str[16] != 'F'):
            euler = euler / 100
        else:
            euler = (65536 - euler) /-100
        pitch = euler

        return {'Yaw': yaw, 'Roll': roll, 'Pitch': pitch}
    
if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__)) + '/GYData'
    print(path)
    # write caption
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['TimeNow',
                         'Acc_X',    'Acc_Y',    'Acc_Z',
                         'Gyro_X',   'Gyro_Y',   'Gyro_Z',
                         'Magnet_X', 'Magnet_Y', 'Magnet_Z',
                         'Yaw',      'Roll',     'Pitch'])

    ser = serial.Serial('/dev/ttyAMA0', 9600)
    GY = GY955(ser)
    time = GY.Time()
    acc = GY.Acc()
    gyro = GY.Gyro()
    magnet = GY.Magnet()
    euler = GY.Euler()
        
    with open(path, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([time,
                         acc['Acc-X'],       acc['Acc-Y'],       acc['Acc-Z'],
                         gyro['Gyro-X'],     gyro['Gyro-Y'],     gyro['Gyro-Z'],
                         magnet['Magnet-X'], magnet['Magnet-Y'], magnet['Magnet-Z'],
                         euler['Yaw'],       euler['Roll'],      euler['Pitch']])