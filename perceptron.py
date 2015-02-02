import math
import random

class Borg:

    __shared_state = {}
    
    def __init__(self):
        self.__dict__ = self.__shared_state

class EventDispatcher:
    """"parent class for objects that should be able to dispatch events"""

    SIGNAL_EVENT = 'signalEvent'

    def __init__(self):
        self.listeners = {}

    def addEventListener(self, eventType, callBack):
        self.listeners.setdefault(eventType,[]).append(callBack)

    def removeEventListener(self, eventType, callBack):
        try:
            self.listeners.setdefault(eventType,[]).remove(callBack)
        except:
            raise ValueError('Error: cant remove event listener: no subsciption to %s from %s' % (eventType, callBack))

    def dispatchEvent(self, eventType, *args, **kwargs):
        #if it has no listeners then fine
        for f in self.listeners.setdefault(eventType,[]):
            f(*args, **kwargs)

class Perceptron(Borg):

    LISTEN_TO   = 0.5       #what part of total sensors should one associate subscribe to if random perceptron
    ASSOCIATES  = 5
    SENSORS     = 8

    """"""
    def __init__(self, sensorSize, associateCount):
        self.sf = SensorField(sensorSize)
        self.associates = [Associate(self.sf, i) for i in range(0, associateCount)]

    def makeDesision(self):
        self.sf.incomingSignal('11111111')
     
        

class Sensor(EventDispatcher):
    """A single sensor of the Sensor Field."""
    """it receives binary signal and dispatches event to any """
    def __init__(self, num):
        super(Sensor, self).__init__()
        self.num = num
        
class SensorField():
    """Input of the Perceptron"""
    """accpets certain number of bits of data"""
    def __init__(self, size):
        self.sensors = []
        self.size = size
        for i in range(0,size):
            self.sensors.append(Sensor(i))

    def incomingSignal(self, signal):
        for i in range(0,len(signal)):
            if int(signal[i])==1: self.sensors[i].dispatchEvent(EventDispatcher.SIGNAL_EVENT)


    def getSensor(self,num):
        return self.sensors[num]



class Associate():
    """A - element of the Perceptron"""
    """It accepts sensor field and starts listening to some number of sensors"""
    
    def __init__(self, sensorField, num):
        self.num = num
        self.w = 0      #weight of A-R link

        #lets subscribe to some of the sensors
        sNums = random.sample([i for i in range(sensorField.size)], math.floor(sensorField.size*Perceptron.LISTEN_TO))
        for i in range(len(sNums)):
            sensor = sensorField.getSensor(sNums[i])
            sensor.addEventListener(EventDispatcher.SIGNAL_EVENT,self.sensorListener)
            
    def sensorListener(self):
        print('Associate listener invoked in Associate',self.num)


class Response():
    """A single sensor of the Sensor Field."""
    """it receives binary signal and dispatches event to any """
    def __init__(self):
        pass

#first lets generate a perceptron
p = Perceptron(sensorSize = Perceptron.SENSORS, associateCount = Perceptron.ASSOCIATES)

#now lets teach it something

p.makeDesision()