from core.log_watcher import LogWatcher
from time import sleep

LOG_PATH = '/var/log/nginx/events_data.log'


seek_previous_lines = True
while True:
    LogWatcher(LOG_PATH, seek_previous_lines).start()

    sleep(1)
    seek_previous_lines = False
