import threading, time

#POURING_ANY = False
start_time = time.time()
sem = threading.Semaphore()

class FlowCalculation():
    def __init__(self,valve_num):
        self.valve_num = valve_num
        self.drink_num = 1
        self.POURING = False
        

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
            threading.Timer(10, self.pour_drink).start()
        #POURING_ANY = False
        sem.release()


    def startSimulation(self):
        global start_time
        start_time=time.time()
        print('simulation started for valve: ' + str(self.valve_num))
        threading.Timer(5, self.pour_drink).start()
