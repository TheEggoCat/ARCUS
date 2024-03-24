from pylablib.devices import Arcus
import sys
import time

#to run, use :: python "Arcus MOTOR.py" [singstep (1 or 0)] [totallength (in inches)] [intervals (int)] [timeatpos (in seconds)]
#ex: python "Arcus MOTOR.py" 1 56.9 10 4.6

#TO DO:
#1: add a limit switch and to first home, move continuously back until limit switch is hit
#   then stop and set that as the home position (aka moveto(0))
#2: Figure out how to use ETHERNET as the docs say there is support for it
#   but don't actually explain what the methods are.


# CONTROLS #

singstep = int(sys.argv[1]) #set mode to single step or to interval (0 or 'else' respectively) 

totallength = float(sys.argv[2]) #how far should the probe move by the end in inch (or cm)
intervals = int(sys.argv[3]) #how many intervals should there be

timeatpos = float(sys.argv[4]) #how long should it spend at each interval position? (in s)

#print(singstep, totallength, intervals, timeatpos) #just a quick check

############

# CONSTS #

MOVETOLENGTH = 000 #factor to convert inch (or cm) to a number for the move method
#to find this move by a random amount and measure how far the brass piece moves physically

MAXLENGTH = 1000000 #how far the probe allowed to extend (in inch (or cm))


##########

#just makes sure you aren't exceeding allowed length
if totallength > MAXLENGTH:
    raise Exception("total move length for the probe exceeds the max allowed length")



tlM = MOVETOLENGTH * totallength #total length in terms of the move command
intervallength = tlM/intervals 
#if singstep = 0, then use tlM, otherwise use intervallength


stage = Arcus.Performax2EXStage()
stage2 = Arcus.GenericPerformaxStage

#home the probe
stage.home()
stage.wait_for_home()

if singstep == 0:
    
    stage.move_by(tlM)
    stage.wait_move()

    time.sleep(timeatpos)

    stage.home()
    stage.wait_for_home()

else:
    for i in range(intervals):
        stage.move_by(intervallength)
        stage.wait_move()

        time.sleep(timeatpos)
    
    stage.home()
    stage.wait_for_home()

stage.close()