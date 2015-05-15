# This gives us control of the Raspberry Pi's pins.
import RPi.GPIO as GPIO

# This is only used for time delays... standard Python stuff
import time

# Tell Pi which pin numbers we'll be using to refer to the GPIO pins.
# We will use the physical pin ordering
GPIO.setmode(GPIO.BOARD)

# We will tell the Broadcom CPU which pins do what.
# There are many pins and most have up to 5 different functions,
# each with a default.  Check the pinout to find non-specialized
# "GPIO" pins.  We'll use P1_Pin_11 (using BOARD reference),
# which is the same as GPIO17 (Broadcom / BCM reference).
# We still just need it to use the GPIO digital function, we just
# need to tell it to designate this pin for OUTPUT.
GPIO.setup(11, GPIO.OUT)

# Now we can use PWM on pin 11.  It's Software PWM, so don't expect perfect
# results.  Linux is a multitasking OS so other processes could interrupt
# the process which generates the PWM signal at any time.
# Raspberry Pi has hardware PWM channel, but this Python library 
# does not yet support it

# Create a PWM control object.
# 11 is the output pin
# 50 is the cycle frequency in Hertz
frequencyHertz = 50
pwm = GPIO.PWM(11, frequencyHertz)

# How to position a servo?  All servos are pretty much the same.
# Send repeated pulses of an absolute duration (not a relative duty cycle)
# between 0.75 ms and 2.5 ms in duration.  A single pulse will only move it
# a short distance in the desired direction.  Repeated pulses will continue
# its movement and then once it arrives at the sprecified position, will
# instruct the motor to forcefully hold its position.

# How to calculate the duty cycle for a specific duration.
# First, know the pulse time for the position you want.
leftPosition = 0.75
rightPosition = 2.5
middlePosition = (rightPosition - leftPosition) / 2 + leftPosition

# I'll store a sequence of positions for use in a loop later on.
positionList = [leftPosition, middlePosition, rightPosition, middlePosition]

# Total number of milliseconds in a cycle.  Given this, we will then
# know both how long we want to pulse in this cycle and how long the 
# cycle itself is. That is all we need to calculate a duty cycle as
# a percentage.
msPerCycle = 1000 / frequencyHertz

# Iterate through the positions sequence 3 times.
for i in range(3):
    # This sequence contains positions from left to right
    # and then back again.  Move the motor to each position in order.
    for position in positionList:
        dutyCyclePercentage = position * 100 / msPerCycle
        print "Position: " + str(position)
        print "Duty Cycle: " + str(dutyCyclePercentage)
        print ""
        pwm.start(dutyCyclePercentage)
        time.sleep(.5)

# Done.  Terminate all signals and relax the motor.
pwm.stop()

# We have shut all our stuff down but we should do a complete
# close on all GPIO stuff.  There's only one copy of real hardware.
# We need to be polite and put it back the way we found it.
GPIO.cleanup()
