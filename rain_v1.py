#TO DO: Ensure short enough watering time and non conflict on water times (separate by at least a minute)
#TO DO: add /static/css/style.css and make it look pretty
#TO DO: Allow /time to also set day of week. radio button, convert to date/year/month.  Show what day it thinks it is now
#TO DO: read crontab to get current program even after loss of power
#TO DO: add USB dongle to get time/date even when power is lost
#TO DO: resize panel/battery to not lose power
#TO DO: sense when barrel is out. switch to city supply (route around pump)
#TO DO: Create BOM

import os
from glob import glob
import time
from datetime import datetime, date
#make the web app work
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (IntegerField, SelectField, RadioField)
from wtforms import widgets, SelectMultipleField
from wtforms.validators import InputRequired, Length
from wtforms.fields import DateField, TimeField
from flask_autoindex import AutoIndex
from crontab import CronTab
import getpass

zones=2 #create arrays below beyond 2, up to 16. But this limits how many we print. Zone 0 is not used.
savedMinute=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
savedHour=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
savedRuntime=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
savedDays=["","","","","","","","","","","","","","","",""]

def createCrons(days,startTime,endTime,zone):
  print("creating crons now")
  cron = CronTab(user=getpass.getuser())
  runTime=datetime.combine(date.today(), endTime) - datetime.combine(date.today(), startTime)
  runTimeSeconds=int(runTime.total_seconds())
  print("run Time is: ",str(runTimeSeconds))
  #daysFormatted="'"+"', '".join(days)+"'"
  daysFormatted="', '".join(days)
  print("days are: ",daysFormatted)
  print("minutes are: ",startTime.minute," hours are: ",startTime.hour)
  #min hour * * day,day,day command
  job = cron.new(command="python3 ~/water/water_v1.py --seconds "+str(runTimeSeconds)+" --zone "+str(zone), comment="Watering Zone "+str(zone))
  job.minute.on(str(startTime.minute))
  job.hour.on(str(startTime.hour))
  for dow in days:
    job.dow.also.on(dow)
  cron.write()
def deleteCrons():
  #cron below not working. try os instead
  user=getpass.getuser()
  os.system("crontab -u "+user+" -l | grep -v 'Watering Zone'  | crontab -u "+user+" -")
  #cron = CronTab(user=getpass.getuser())
  #for job in cron:
  #  print(job)
  #  jobText=str(job)
  #  if 'Watering Zone' in jobText:
  #    print("removing old cron: ",job)
  #    cron.remove( job )
  #cron.remove_all('water_v1.py')
  #cron.remove_all(comment='Watering Zone')
def readCrons():
  global savedMinute, savedHour, savedDays, savedRuntime, zones
  cron = CronTab(user=getpass.getuser())
  jobs = cron.find_command('water/water')
  index = 1
  for job in jobs:
    jobText=str(job)
    jobTextArray=jobText.split()
    savedMinute[index]=str(job.minute)
    savedHour[index]=str(job.hour)
    savedDays[index]=str(job.dow)
    savedRuntime[index]=str(jobTextArray[8])
    index = index + 1
def resetCurrentTime(currentTime):
  print("Setting system time to: ",currentTime.strftime("%H:%M"))
  date_cmd = 'sudo date --set=\"20240410 '+str(currentTime.hour)+':'+str(currentTime.minute)+'\"'
  print("Command: "+date_cmd)
  os.system(date_cmd)

SECRET_KEY = 'rainkey'
app = Flask(__name__)

app.config.from_object(__name__)
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
class rainForm(FlaskForm):
    days1 = MultiCheckboxField('Days', choices=[('MON','Mon'),('TUE','Tue'),('WED','Wed'),('THU','Thu'),('FRI','Fri'),('SAT','Sat'),('SUN','Sun')])
    startTime1 = TimeField('Start Time', format='%H:%M')
    endTime1 = TimeField('End Time', format='%H:%M')
    days2 = MultiCheckboxField('Days', choices=[('MON','Mon'),('TUE','Tue'),('WED','Wed'),('THU','Thu'),('FRI','Fri'),('SAT','Sat'),('SUN','Sun')])
    startTime2 = TimeField('Start Time', format='%H:%M')
    endTime2 = TimeField('End Time', format='%H:%M')
class timeForm(FlaskForm):
	currentTime = TimeField('Current Time', format='%H:%M') #took out - problems: , default=datetime.now().strftime("%H:%M:%S")

@app.route('/',methods=['post','get'])
def run():
  global savedMinute, savedHour, savedRuntime, savedDays, zones, job1, job2
  form = rainForm()
  if form.validate_on_submit():
    print("Raw input values are:")
    print(form.days1.data)
    print(form.startTime1.data)
    print(form.endTime1.data)
    print(form.days2.data)
    print(form.startTime2.data)
    print(form.endTime2.data)
    #Check for errors and do the work
    deleteCrons()
    createCrons(form.days1.data,form.startTime1.data,form.endTime1.data,1)
    createCrons(form.days2.data,form.startTime2.data,form.endTime2.data,2)
  else:
    print(form.errors)
  readCrons()
  return render_template('rain.html',datetime = str(datetime.now().strftime("%H:%M")),
    savedDaysTem1=str(savedDays[1]),savedStartTimeTem1=str(savedHour[1])+":"+str(savedMinute[1]),savedRuntimeTem1=str(savedRuntime[1]),
    savedDaysTem2=str(savedDays[2]),savedStartTimeTem2=str(savedHour[2])+":"+str(savedMinute[2]),savedRuntimeTem2=str(savedRuntime[2]),form=form)

@app.route('/time',methods=['post','get'])
def time():
  form = timeForm()
  if form.validate_on_submit():
    print("Raw input values are:")
    print(form.currentTime.data)
    #Check for errors and do the work
    resetCurrentTime(form.currentTime.data)
  else:
    print(form.errors)
  return render_template('time.html',datetime = str(datetime.now().strftime("%H:%M")),form=form)

if __name__ == '__main__':
  app.run(debug=True)
