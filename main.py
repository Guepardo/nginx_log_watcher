from core.log_watcher import LogWatcher
LOG_PATH = 'test.txt'


seek_previous_lines = True
while True:
    LogWatcher(LOG_PATH, seek_previous_lines).start()
    seek_previous_lines = False
