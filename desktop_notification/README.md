# During the lockdown my PC battery was not working properly it automatically went off on exatly 50% battery
## sometimes it went of while I am working  

# So I made this python project for my help 😎

It automatically run in the background when I open the PC and checks if charging is pluged in or not 
if not it shows a notification 5 times in a row with intervel of 10 sec 

## like This, Just for representation I change some variables 😎
<img src='https://github.com/rishabhjainfinal/some_random_projects/blob/main/desktop_notification/example.png'>

## Setup for autorun program on starting the PC
After the windows boots up it runs (equivalent to double-clicking) all the application present in its startup directory.

Address:
`C:\Users\current_user\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\`

**By default the AppData folder under the current_user is hidden so enable hidden files to get it and paste the shortcut of the script in the given address or the script itself. Also the .PY files default must be set to python IDE else the script may end up opening as a text instead of executing.**

### These are the variable inside the program you can edit for different results 
alert_percent = 75    # batter percent you wanna notify

notification_limit = 5  # you can change this variable for more or less notifications

### requirements 
```
pip install win10toast psutil
```
------------
# Hope it seems interesting ^_^
