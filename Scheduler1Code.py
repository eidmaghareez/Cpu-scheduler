import operator
import sys
#Data structure for process
class pcb:
  def setfirstrunRR(self,firstrun):
      if (self.isfirstrunset==False):
        self.setfirstrun(firstrun)
        self.isfirstrunset=True
      
  def getid(self):
    global id
    id+=1
    return id
  def setfirstrun(self,firstrun):
    self.firstrun=firstrun
  def setfinishtime(self,finishtime):
    self.finishtime=finishtime
  def __init__(self,bursts,arrivetime,priority=0,isfirstrunset=False):
    self.priority=priority
    self.bursts=bursts
    self.priority=priority
    self.id=self.getid()
    self.arrivetime=arrivetime
    self.isfirstrunset=isfirstrunset
    
  def processinfo(self):
    print("process id ",self.id," priority ",self.priority," bursts ", self.bursts," arrivetime ",self.arrivetime)
  def processfinalinfo(self):
    print("process id ",self.id," priority ",self.priority," bursts ", self.bursts," arrivetime ",self.arrivetime," first run : ",self.firstrun," finishtime : ",self.finishtime)


#Functions for PR
def priorityqueue(readyqueue):
    global time
    curr=readyqueue[0]
    curr.setfirstrun(time)
    time+=curr.bursts
    curr.setfinishtime(time)
    return(readyqueue.pop(0))
def outputPR(algorithm,inputfilename,processes):
    print("Input file name : ",inputfilename)
    print("Algorithm :",algorithm)
    print("Avg.turnaround time: ",avgturnaround(processes),"ms")
    print("Avg.response time: ",avgresponse(processes),"ms")
    print("Cpu timeline : ")
    for i in processes:
     print("process (id):",i.id,"(start:",i.firstrun,"-> finish:",i.finishtime,")")

#Functions for RR
def roundrobin(readyqueue):
  out=[]
  global time
  global quantum
  curr=readyqueue[0]
  if(curr.arrivetime<=time):
    curr.setfirstrunRR(time)
    temptime=time
    if(curr.bursts<quantum):
      time+=quantum-curr.bursts
      curr.bursts=0
    else:
      time+=quantum
      curr.bursts-=quantum
    timeline="process (id): "+str(curr.id)+" ("+str(temptime)+"->"+str(time)+")"
    if(curr.bursts<=0):
      curr.setfinishtime(time)
      out.append(True)
      out.append(readyqueue.pop(0))
      out.append(timeline)
      return out
    else:
     readyqueue.append(readyqueue.pop(0))
     out.append(False)
     out.append(1)
     out.append(timeline)
     return out
  else:
    readyqueue.append(readyqueue.pop(0))
    out.append(False)
    out.append(0)
    return out
def outputRR(algorithm,inputfilename,processes,quantum,timelineprint):
    print("Input file name : ",inputfilename)
    print("Algorithm :",algorithm,"(",quantum,")")
    print("Avg.turnaround time: ",avgturnaround(processes),"ms")
    print("Avg.response time: ",avgresponse(processes),"ms")
    print("Cpu timeline :")
    for i in timelineprint:
      print(i)

#Function to create processes
def createprocess(algorithm,bursts,arrivetime,priority=0):
  if(algorithm=="RR"):
   process=pcb(bursts,arrivetime)
  else:
   process=pcb(bursts,arrivetime,priority)
  return process
#Functions for calculations
def avgturnaround(list):
  numberofprocesses=len(list)
  turnaroundsum=0
  for i in list:
    turnaroundsum+=(i.finishtime-i.arrivetime)
  return (turnaroundsum/numberofprocesses)
def avgresponse(list):
  numberofprocesses=len(list)
  responsesum=0
  for i in list:
    responsesum+=(i.firstrun-i.arrivetime)
  return (responsesum/numberofprocesses)
#inputs
algorithm= str((sys.argv[1]))
quantum= int(sys.argv[2])
inputfilename=str((sys.argv[3]))
#preparing inputs to be processed
file=open(inputfilename,"r")
input=file.readlines()
inputfixed=[]
id=0
time=0
arrivetime=0
readyqueue=[]
timeline=[]
for i in input:
  inputfixed.append(i.rstrip())

for i in inputfixed:
  if(i[:4]=="proc"):
    integersininput=i[5:].split(" ")
    integersininput=list(map(int,integersininput))
    priority=integersininput[0]
    bursts=integersininput[1]
    process=createprocess(algorithm,bursts,arrivetime,priority)
    readyqueue.append(process)
    #Sorting processes depending on priority and if same priority by id <-lower id means arrived first
    if (algorithm=="PR"):
      readyqueue = sorted(readyqueue,key=operator.attrgetter("priority", "id"))
    #sorting processes depending on arrive time in RR
    else:
      readyqueue = sorted(readyqueue,key=operator.attrgetter("id"))
  
  elif(i[0:4]=="idle"):
    idle=int(i[5:])
    arrivetime+=idle
  else:
    break;
if(algorithm=="PR"):
  while (readyqueue):
    timeline.append(priorityqueue(readyqueue))
  outputPR(algorithm,inputfilename,timeline)
if(algorithm=="RR"):
  timelineprint=[]
  while(readyqueue):
    temp=roundrobin(readyqueue)
    if(temp[0]==True):
      timeline.append(temp[1])
    if(temp[1]!=0):
      timelineprint.append(temp[2])
  outputRR(algorithm,inputfilename,timeline,quantum,timelineprint)
