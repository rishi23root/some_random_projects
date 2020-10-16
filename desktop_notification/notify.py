# pip install win10toast,psutil
import psutil
from win10toast import ToastNotifier
import time

alert_percent = 75    # batter percent you wanna 
notification_limit = 5  # you can change this variable for more or less notifications

title = "Battery Percentage Alert !!!!!!!"

def show_notification(title,message,duration = 10,icon_path = "./image.ico" ):
	# createing notification box
	toaster = ToastNotifier()
	# parameters
	# title,message ,image path in .ico,duration in sec,bool threading
	toaster.show_toast(title,mess,icon_path=icon_path,duration=duration)


count = 0 # creaing limit of 5 notifications only with interval of 10 sec each
while count <= notification_limit and not psutil.sensors_battery().power_plugged :
	# extracting battery info 
	battery = psutil.sensors_battery()
	battery_percent = battery.percent
	plugged = battery.power_plugged

	# check if bettery is less then 75% and not pluged 
	if battery_percent <= alert_percent and not plugged :
		count += 1      
		mess = "computer is about to went off \npower is not pluged in \nand battery is only {}% left \nbetter pluged in fast".format(battery_percent)
		show_notification(title,mess)
		print('notification shown')
		time.sleep(10)
		# alert by notification
	else :
		print('sleep')
		time.sleep(10)
