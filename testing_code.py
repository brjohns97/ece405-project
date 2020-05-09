class FlowCalculation():
    def __init__(self):
        self.pour_time = 69
        
    def changePourTime(self):
        self.pour_time = 420
    
    def startSimulation(self):
        self.changePourTime()
    def initializeData(self,form):
        self.pour_time = form.pour_time
        
        
f1 = FlowCalculation()
f2= FlowCalculation()

print(f1.pour_time)
f1.startSimulation()
print(f1.pour_time)
print(f2.pour_time)

def createFlowObject():
    f2.initializeData(f1)

createFlowObject()
print(f2.pour_time)