import threading, time

#POURING_ANY = False
start_time = time.time()
sem = threading.Semaphore()

class FlowCalculation():
    def __init__(self,valve_num):
        self.valve_num = valve_num
        self.drink_num = 1
        self.POURING = False
        self.valve_thread = 0
        self.CANCELED_FLAG=0
        self.keg_stats = {
            'pour_check':0,
            'start_check':0,
            'valve_number':self.valve_num,
            'drinks':13
        }

    def pour_drink(self):
        #global POURING_ANY
        #while((POURING_ANY) == True):
        #    time.sleep(1)
        #POURING_ANY = True
        global start_time, sem
        sem.acquire()
        if(self.drink_num < 6):
            print('start... valve: ' + str(self.valve_num) + '  drink#: ' + str(self.drink_num) + '  time: ' + str(time.time()-start_time))
            self.POURING = True
            time.sleep(3)
            self.POURING = False
            print('ended... valve: ' + str(self.valve_num) + '  drink#: ' + str(self.drink_num) + '  time: ' + str(time.time()-start_time))
            self.drink_num=self.drink_num+1
            time.sleep(2.5)
            if(self.CANCELED_FLAG==0):
                self.valve_thread = threading.Timer(10, self.pour_drink)
                self.valve_thread.start()
            else:
                self.CANCELED_FLAG=0
        #POURING_ANY = False
        sem.release()

    def scheduleSimulation(self):
        print('simulation scheduled for valve: ' + str(self.valve_num))
        self.valve_thread = threading.Timer(10, self.startSimulation)
        self.valve_thread.start()

    def startSimulation(self):
        global start_time
        start_time=time.time()
        print('simulation started for valve: ' + str(self.valve_num))
        self.valve_thread = threading.Timer(5, self.pour_drink)
        self.valve_thread.start()
        
    def cancel_valve(self):
        self.CANCELED_FLAG=1
        print('canceling for valve: ' + str(self.valve_num))
        print(self.valve_thread)
        self.valve_thread.cancel()
