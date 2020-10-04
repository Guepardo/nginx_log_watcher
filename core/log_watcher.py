import os
from time import sleep
from workers.sender import Sender


class LogWatcher:
    READ_FILE_FREQUECY_IN_SECONDS = 1
    LIMIT_BATCH_SIZE = 10

    def __init__(self, log_path, seek_previous_lines=True):
        self.log_path = log_path
        self.seek_previous_lines = seek_previous_lines
        self.logs = []

    def file_identifier(self):
        return os.stat(self.log_path).st_ino

    def start(self):
        last_file_identifier = self.file_identifier()

        with open(self.log_path, 'r') as arq:
            if self.seek_previous_lines:
                arq.seek(0, os.SEEK_END)

            while True:
                if last_file_identifier != self.file_identifier():
                    return

                for line in arq.readlines():
                    self.logs.append(line)

                if len(self.logs) > self.LIMIT_BATCH_SIZE:
                    Sender(self.logs).start()
                    self.logs = []

                sleep(self.READ_FILE_FREQUECY_IN_SECONDS)
