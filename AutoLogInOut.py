import threading
from loginout_scheduler import schedule_start, check_time, schedule_end
from autologin import login
from autologout import logout
import pystray
from PIL import Image
import os
import sys


if getattr(sys, 'frozen', False):
    #test.exe로 실행한 경우,test.exe를 보관한 디렉토리의 full path를 취득
    curr_path = os.path.dirname(os.path.abspath(sys.executable))
else:
    #python test.py로 실행한 경우,test.py를 보관한 디렉토리의 full path를 취득
    curr_path = os.path.dirname(os.path.abspath(__file__))


def tray_end():
    schedule_end[0] = True


menu = pystray.Menu(pystray.MenuItem("TimeCheck", check_time),
                    pystray.MenuItem("LogIn", lambda : login(False,True)),
                    pystray.MenuItem("LogOut", lambda : logout(True)),
                    pystray.MenuItem("Quit", tray_end))
image = Image.open(curr_path+"/auto.png")
icon = pystray.Icon(name = "Auto", icon = image, title="Auto", menu = menu)

tray = threading.Thread(target=icon.run)
tray.setDaemon(True) 
tray.start()
schedule_start()
