import time
from datetime import datetime
from module.eaeo import constant as mcs
from module.eaeo import common as mcm

def instagram_sync_scheduler():
    while 1:
        print("====> task started")
        time.sleep(mcs.instagram_sync_period)
        now = datetime.now()
        weekday = now.weekday()
        hour = now.hour
        # 0 o'clock on Saturday
        if weekday != 5 or hour != 0:
            continue

        print("====> start syncing")
        res = mcm.scheduled_sync_instagram_accounts()
        print("====> syncing ended")
        if res == 1:
            print("====> success to sync all")
        else:
            print("====> fail to sync one of handles")