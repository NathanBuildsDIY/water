from gpiozero import Device, PhaseEnableMotor, Robot, PhaseEnableRobot, LED, Servo, AngularServo, Button, PWMLED
#from gpiozero.pins.pigpio import PiGPIOFactory
import datetime
import time

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--seconds", help="Number of seconds to turn on pump",type=int, default="10")
parser.add_argument("--zone", help="Zone to turn on =",type=int, default="1")
args = parser.parse_args()

#factory = PiGPIOFactory()
#pump = AngularServo(10, initial_angle=0, min_angle=0, max_angle=180, min_pulse_width=4/10000, max_pulse_width=25/10000,pin_factory=factory)
#pump = PWMLED(12, initial_value = 0, pin_factory = factory) #only if factory works - pi zero

cityWater = LED(27)
rainWater = LED(22)
rainBarrelFull = Button(26)
pump = LED(17)
if args.zone == 1:
  zoneValve = LED(23)
if args.zone == 2:
  zoneValve = LED(24)
  
now = datetime.datetime.now()
print("starting pump now for these seconds: ",args.seconds)
print(now)
#pump.blink(on_time=args.seconds,off_time=1,fade_in_time=1,fade_out_time=1)
#pump.blink(1,1,1,1,2,True)
zoneValve.on()
time.sleep(0.5) #let valve open before we pump
if rainBarrelFull.is_pressed:
  rainWater.on()
  time.sleep(0.5)
  pump.on()
  time.sleep(args.seconds)
  pump.off()
  time.sleep(0.5)
  rainWater.off()
else:
  cityWater.on()
  time.sleep(args.seconds)
  cityWater.off()
  time.sleep(0.5)
zoneValve.off()
now = datetime.datetime.now()
print("turning off pump now for zone: ",args.zone)
print(now)
