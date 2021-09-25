# lift movement: going up = 1; going down = -1; still = 0;
# input after running the code is like this 5 2 1 this means 5 floors 2 elevators and 1 time unit
#time is 1 unit can change it into 10m
#after inital run inputs are BUN or BDN which represents the button to go up ot button to go down N is the floor you want to go to
#AUN,ADN,AON,ASN represents elevator N going up, going down, opening dooor,staticor idel
#taken in to consideration about electricity cost also  
import time
start_time = time.time()
class newLift:      
	def __init__(self,totalFloors):    #used to initilize all the factors in this design
		halts=[]
		while totalFloors>=0:
			halts.append(0)
			totalFloors=totalFloors-1
			pass
		self.number=0
		self.direction=0
		self.currentFloor=1
		self.halts=halts
		self.destination=1
		self.working=0

class lobbyStatus:
	def __init__(self,totalFloors): #initilize the different lobby which will house the 2 or more elevators
		upBtns=[]
		downBtns=[]
		while totalFloors>=0:
			upBtns.append(0)
			downBtns.append(0)
			totalFloors=totalFloors-1
			pass
		self.upBtns=upBtns
		self.downBtns=downBtns

def inside(lift,actions):       #contians the logic for chosing the AS,AD,AU actions.
	if lift.direction==0:
		if lift.destination==lift.currentFloor: #if lift is not moving
			actions.append("AS"+str(lift.number))
			pass
		else:
			if lift.currentFloor-lift.destination>0:
				lift.direction=-1
				lift.currentFloor=lift.currentFloor-1
				actions.append("AD"+str(lift.number))
				pass
			else:
				lift.direction=1
				lift.currentFloor=lift.currentFloor+1
				actions.append("AU"+str(lift.number))
			pass
		pass
	elif lift.direction==1:                    #lift is moving up. here we have inner states of opening door depending on going up
		if lift.halts[lift.currentFloor]==1:
			if lift.currentFloor==len(lift.halts)-1:
				actions.append("AOD"+str(lift.number))
				lift.direction=0
				lift.halts[lift.currentFloor]=0
				lobby_1.downBtns[lift.currentFloor]=0
				pass
			elif lift.destination==lift.currentFloor:
				if lobby_1.upBtns[lift.currentFloor]==1:
					actions.append("AOU"+str(lift.number))
					lift.halts[lift.currentFloor]=0
					lobby_1.upBtns[lift.currentFloor]=0
					pass
				elif lobby_1.downBtns[lift.currentFloor]==1:
					actions.append("AOD"+str(lift.number))
					lift.halts[lift.currentFloor]=0
					lift.direction=-1
					lobby_1.downBtns[lift.currentFloor]=0
					pass
				else:
					actions.append("AS"+str(lift.number))
					lift.halts[lift.currentFloor]=0
					lift.direction=0
					pass
				pass
			else:
				actions.append("AOU"+str(lift.number))
				lift.halts[lift.currentFloor]=0
				lobby_1.upBtns[lift.currentFloor]=0
				pass
			pass
		else:
			if lift.currentFloor==len(lift.halts)-1:
				actions.append("AS"+str(lift.number))
				lift.direction=0
				lift.destination=lift.currentFloor
				pass
			elif lift.currentFloor==lift.destination:
				actions.append("AS"+str(lift.number))
				lift.direction=0
			else:
				actions.append("AU"+str(lift.number))
				lift.currentFloor=lift.currentFloor+1
				pass
			pass
		pass
	else:                                      #lift is going down
		if lift.halts[lift.currentFloor]==1:
			if lift.currentFloor==1:
				actions.append("AOU"+str(lift.number))
				lift.direction=0
				lift.halts[lift.currentFloor]=0
				lobby_1.upBtns[lift.currentFloor]=0
				pass
			elif lift.destination==lift.currentFloor:
				if lobby_1.downBtns[lift.currentFloor]==1:
					actions.append("AOD"+str(lift.number))
					lift.halts[lift.currentFloor]=0
					lobby_1.downBtns[lift.currentFloor]=0
					pass
				elif lobby_1.upBtns[lift.currentFloor]==1:
					actions.append("AOU"+str(lift.number))
					lift.halts[lift.currentFloor]=0
					lift.direction=1
					lobby_1.upBtns[lift.currentFloor]=0
					pass
				else:
					actions.append("AS"+str(lift.number))
					lift.halts[lift.currentFloor]=0
					lift.direction=0
				pass
			else:
				actions.append("AOD"+str(lift.number))
				lift.halts[lift.currentFloor]=0
				lobby_1.downBtns[lift.currentFloor]=0
				pass
			pass
		else:
			if lift.currentFloor==1:
				actions.append("AS"+str(lift.number))
				lift.direction=0
				lift.destination=1
				pass
			elif lift.currentFloor==lift.destination:
				actions.append("AS"+str(lift.number))
				lift.direction=0
			else:
				actions.append("AD"+str(lift.number))
				lift.currentFloor=lift.currentFloor-1
				pass
			pass
		pass
	pass

def actionState_0(lift,floor): #action used to descide what to do when the lift is in halt state 
	lift.destination=floor
	lift.halts[floor]=1
	relavtivePosition=floor-lift.currentFloor
	if relavtivePosition==0:
		if lobby_1.upBtns[lift.currentFloor]==1:
			lift.direction=1
			pass
		else:
			lift.direction=-1
			pass
		pass
	elif relavtivePosition>0:
		lift.direction=1
		pass
	else:
		lift.direction=-1
		pass
	pass


def actionState_1(movingLift,floor,direction,stillLift):#state transition  
	lift=movingLift
	reqDirection_1=direction
	if lift.currentFloor-floor>0:
		reqDirection_2=-1
		pass
	else:
		reqDirection_2=1
		pass

	if (lift.currentFloor==floor) & (reqDirection_1==lift.direction):
		lift.halts[floor]=1
		pass
	elif reqDirection_1==reqDirection_2==lift.direction:
		if lift.direction==1:
			if lift.destination<floor:
				lift.destination=floor
				pass
			lift.halts[floor]=1
			pass
		else:
			if lift.destination>floor:
				lift.destination=floor
				pass
			lift.halts[floor]=1
			pass
		pass
	else:
		actionState_0(stillLift,floor)
		pass
	pass

def actionState_2(liftA,liftB,floor,direction):#used to define which direction and which elevator should serve the request during arrival mode
	if (liftA.currentFloor==floor) & (liftA.direction==direction):
		liftA.halts[floor]=1
		pass
	elif (liftB.currentFloor==floor) & (liftB.direction==direction):
		liftB.halts[floor]=1
		pass
	elif floor-liftA.currentFloor==liftA.direction==direction:
		liftA.halts[floor]=1
		if liftA.direction==1:
			if liftA.destination<floor:
				liftA.destination=floor
				pass
			pass
		else:
			if liftA.destination>floor:
				liftA.destination=floor
				pass
			pass
		pass
	elif floor-liftB.currentFloor==liftB.direction==direction:
		liftB.halts[floor]=1
		if liftB.direction==1:
			if liftB.destination<floor:
				liftB.destination=floor
				pass
			pass
		else:
			if liftB.destination>floor:
				liftB.destination=floor
				pass
			pass
		pass
	pass

def updateLift(lift,floor): #update the parameters of the lift in the loop
	lift.halts[floor]=1
	if lift.direction==1:
		if lift.destination<floor:
			lift.destination=floor
			pass
		pass
	else:
		if lift.destination>floor:
			lift.destination=floor
			pass
		pass
	pass

parameters=input().split()#gets the input of the program
N=int(parameters[0])
K=int(parameters[1])
#p=parameters[2]
#q=parameters[3]
#r=parameters[4]
tu=parameters[2]

lift_1=newLift(N)
lift_1.number=1

lift_2=newLift(N)
lift_2.number=2

lift_3=newLift(N)
lift_3.number=3

lobby_1=lobbyStatus(N)

if K>0:
	lift_1.working=1
	pass
if K>1:
	lift_2.working=1
	pass
if K>2:
	lift_3.working=1
	pass

print(0)

while True:
	actions=[]
	tasks=[x.upper() for x in input().split()] #used to get the user inputs with respect to which button

	while tasks:
		task=tasks[0]
		if len(task)>1:
			if task[1]=="U":
				lobby_1.upBtns[int(task[2])]=1
				pass
			elif task[1]=="D":
				lobby_1.downBtns[int(task[2])]=1
				pass
			else:
				if int(task[2])==1:
					updateLift(lift_1,int(task[1]))
				elif int(task[2])==2:
					updateLift(lift_2,int(task[1]))
				else:
					updateLift(lift_3,int(task[1]))
				pass
			pass
		tasks.pop(0)
		pass

	for x in range(1,N):
		if lobby_1.upBtns[x]==1:
			state=abs(lift_1.direction)+abs(lift_2.direction)
			if state==0:
				if abs(lift_1.currentFloor-x)<=abs(lift_2.currentFloor-x):
					actionState_0(lift_1,x)
					pass
				else:
					actionState_0(lift_2,x)
					pass
				pass
			elif state==1:
				if lift_1.direction!=0:
					actionState_1(lift_1,x,1,lift_2)
					pass
				else:
					actionState_1(lift_2,x,1,lift_1)
				pass
			elif state==2:
				actionState_2(lift_1,lift_2,x,1)
			pass
		pass

	for y in range(0,N-1):
		x=N-y
		if lobby_1.downBtns[x]==1:
			state=abs(lift_1.direction)+abs(lift_2.direction)
			if state==0:
				if abs(lift_1.currentFloor-x)<=abs(lift_2.currentFloor-x):
					actionState_0(lift_1,x)
					pass
				else:
					actionState_0(lift_2,x)
					pass
				pass
			elif state==1:
				if lift_1.direction!=0:
					actionState_1(lift_1,x,-1,lift_2)
					pass
				else:
					actionState_1(lift_2,x,-1,lift_1)
				pass
			else:
				actionState_2(lift_1,lift_2,x,-1)
			pass
		pass

	inside(lift_1,actions)
	inside(lift_2,actions)
	action=""
	while actions:
		if action=="":
			action=actions[0]
			pass
		else:
			action=action+" "+actions[0]
		actions.pop(0)
		pass
	print("---------------------------------------------")
	print(action)
	print("---------------------------------------------")
	print("lift_1 is on floor: ",lift_1.currentFloor)
	print("lift_1 is moving in direction: ",lift_1.direction)
	print("lift_1's halts: ",lift_1.halts)
	print("lift_1's destination: ",lift_1.destination)
	print("---------------------------------------------")
	print("lift_2 is on floor: ",lift_2.currentFloor)
	print("lift_2 is moving in direction: ",lift_2.direction)
	print("lift_2's halts: ",lift_2.halts)
	print("lift_2's destination: ",lift_2.destination)
	print("---------------------------------------------")
	print("lobby_1's up buttons:",lobby_1.upBtns)
	print("lobby_1's down buttons:",lobby_1.downBtns)
	print("---------------------------------------------")
    
	pass
print("--- %s seconds ---" % (time.time() - start_time))