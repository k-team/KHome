import sys
import time
import math
import random

cd = sys.path.pop(0)
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
sys.path.insert(0, cd)

def Dummy(dummy_funct):
    """
    Return a class generating dummy data describe by the *dummy_funct* function.
    *dummy_funct* receive the time as parameter and return one value
    """

    class _Dummy(object):
        def acquire_value(self):
            return dummy_funct(time.time())
    return _Dummy

# TemperatureSensor = Dummy(lambda t:
#         math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))

#DoorSensor = Dummy(
#        True if random.random() > 0.5 else False)


Air = Dummy(lambda t:
        math.sin(t) * 30 + 30 + 0.5 * (random.random() - 0.5))

Butane = Dummy(lambda t:
        math.sin(t) * 1500 + 2000 + 0.5 * (random.random() - 0.5)) #seuil 1500

CO = Dummy(lambda t:
        math.sin(t) * 200 + 200 + 0.5 * (random.random() - 0.5)) # seuil 60

Camera = Dummy(lambda t:
        math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))

ElectricCurrent = Dummy(
        True if random.random() > 0.5 else False)

LightButton = Dummy(
        True if random.random() > 0.5 else False)

LuminosityExterior = Dummy(lambda t:
        math.sin(t) * 800 + 820 + 0.5 * (random.random() - 0.5)) #seuil a fixer

Methane = Dummy(lambda t:
        math.sin(t) * 600 + 800 + 0.5 * (random.random() - 0.5)) #seuil max 1000

Moisture = Dummy(lambda t:
        math.sin(t) * 20 + 35 + 0.5 * (random.random() - 0.5)) #seuil max 45

OutsideBrightness = Dummy(lambda t:
        math.sin(t) * 800 + 820 + 0.5 * (random.random() - 0.5)) #seuil a fixer

Propane = Dummy(lambda t:
        math.sin(t) * 1500 + 2000 + 0.5 * (random.random() - 0.5)) #seuil 1500

RainForecast = Dummy(
        True if random.random() > 0.5 else False)

Shutter = Dummy(lambda t:
        math.sin(t) * 50 + 50 + 0.5 * (random.random() - 0.5))

Smoke = Dummy(lambda t:
        math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))

Sound = Dummy(lambda t:
        math.sin(t) * 60 + 60 + 0.5 * (random.random() - 0.5)) #seuil cri nourison fixe a 97dBl

TemperatureForecast = Dummy(lambda t:
        math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))

TemperatureExterior = Dummy(lambda t:
        math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))




class SensorConnection(Protocol):

    def __init__(self, sensor, filter_id):
        self.sensor = sensor
        self.filter_id = filter_id
        
    def connectionMade(self):
        print "Connexion etablished"

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        #print "Server said:", data
        self.analyser(data)
    
    def connectionLost(self, reason):
        print "connection lost"
      
    def analyser(self,data):
        print "analyse en cours: "
        #a completer
        org = data[6:8]
    valeur = '{0:032b}'.format(int(data[8:16],16))
    sensor_id = data[16:24]
    status = '{0:08b}'.format(int(data[24:26],16))
    checksum = '{0:08b}'.format(int(data[26:28],16))

    if sensor_id == self.filter_id:
        print "id: " + sensor_id
        print "serveur said: " + data
        if org == "05":
            #todo
            sentData = self.org05(valeur,status)
            #self.sensor.emit_value(sentData)
        if org == "06":
            #todo
            sentData = self.org06(valeur)
            #self.sensor.emit_value(sentData) 
        if org == "07":
            #todo
            if sensor_id[4:8] == "3E7B":
                print "c'est un capteur de lumiere"
                sentData = self.org7_lumiosite_presence(valeur)
                print sendData
                #self.sensor.emit_value(sentData) 
            elif sensor_id == "00893378":
                print "c'est un capteur de temperature et humidite"
                sentData = self.org7_temp_humi(valeur)
                print sendData
                #self.sensor.emit_value(sentData) 
            
    def org7_lumiosite_presence(self, valeur): #ordre des octets: DB0 DB1 DB2 DB3 mais pas DB3 DB2 DB1 DB0
        lumiosite = int(valeur[16:24],2)*510/255
        temp = int(valeur[8:16],2)*51/255
        presence = 1
        if valeur[1]=="1":
            presence = 0
        ls = [lumiosite,temp,presence]
        return ls
            
    def org7_temp_humi(self, valeur): #ordre des octets: DB0 DB1 DB2 DB3 mais pas DB3 DB2 DB1 DB0
        humi = int(valeur[16:24],2)*100/250 #use DB2
        l=[]
        l.append(humi)
        if valeur[1] =="0":
            l.append(-1)
        else:
            temp = int(valeur[8:16],2)*40/250 #use DB1
            l.append(temp)
        return l 
        
    
    def org06(self,valeur):
        if valeur[31]=="0":
            print "ouvert" 
            return 0
        else:
            print "ferme"
            return 1
        
    def findButton(self,b):
        if b=="001":
            return 0b1000
        elif b == "000":
            return 0b0100 #A1
        elif b == "010":
            return 0b0001 #"B1"
        elif b == "011":
            return  0b0010 #"B0"
        else:
            return 0b0000
     
    def org05(self,valeur,status):
        if status[3]=="1":
            #trouver des boutons presser
            b1 = valeur[0:3]  #button 1
            if (valeur[7] =="0" and valeur[3]=="1"): #1 seul bouton presse
                print "les boutons appuyes: ",self.findButton(b1)
                return self.findButton(b1)
            elif valeur[7] == "1": # deux boutons presser
                b2 = valeur[4:7] #button 2
                print "les deux boutons appuyes: ",self.findButton(b1)|self.findButton(b2)
                return self.findButton(b1)|self.findButton(b2)
        else:
            #verifier si les boutons qui ont ete presser sont relacher
            print "les boutons relaches: ",0b0000
            return 0b0000
            
                    
            
class SensorConnectionFactory(ClientFactory):
    def __init__(self, sensor, filter_id):
        self.sensor = sensor
        self.filter_id = filter_id

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
# Do something ?

    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
# Do something ?

    def buildProtocol(self, addr):
        return SensorConnection(self.sensor, self.filter_id)

class Sensor(object):
    sensor_host = '134.214.106.23'
    sensor_port = 5000

    def __init__(self,sensor_id):
        super(Sensor, self).__init__()
        reactor.connectTCP(type(self).sensor_host,
                type(self).sensor_port,
                SensorConnectionFactory(self,
                    sensor_id))

    def start(self):
        #super(Sensor, self).start()
        reactor.run()

    def close(self):
        super(Sensor, self).close()

if __name__ == '__main__':
    sensor = Sensor("0021CC31")
    sensor.start()
