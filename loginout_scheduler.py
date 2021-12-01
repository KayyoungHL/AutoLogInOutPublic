import time
import schedule
from autologin import login
from autologout import logout
import random


schedule_end = [False]

def init():
    schedule.clear()
    login_time = f"08:{random.randint(0,40):0>2}:{random.randint(0,59):0>2}"
    logout_time = f"18:{random.randint(1,4):0>2}:{random.randint(0,59):0>2}"
    schedule.every().day.at(login_time).do(login, True, True)
    schedule.every().day.at(logout_time).do(logout, True)
    schedule.every().day.at("06:00:00").do(init)


def check_time():
    print(schedule.get_jobs())


def schedule_start():
    init()
    while True:
        schedule.run_pending()
        time.sleep(1)
        if schedule_end[0]:break


if __name__ == "__main__":
    schedule_start()