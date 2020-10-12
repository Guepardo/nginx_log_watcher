import os
from time import sleep
from workers.sender import Sender


class LogWatcher:
    READ_FILE_FREQUECY_IN_SECONDS = 30

    def __init__(self, log_path, seek_previous_lines=True):
        self.log_path = log_path
        self.seek_previous_lines = seek_previous_lines
        self.logs = []

    def log_file_stat(self):
        return os.stat(self.log_path)

    def log_file_changed(self):
        current_log_file_stat = self.log_file_stat()

        print("{} != {} -- {} < {}".format(self.last_file_check.st_ino,
                                           current_log_file_stat.st_ino,
                                           self.last_file_check.st_size,
                                           current_log_file_stat.st_size)
              )

        changed = self.last_file_check.st_ino != current_log_file_stat.st_ino or \
            self.last_file_check.st_size > current_log_file_stat.st_size

        self.last_file_check = current_log_file_stat
        return changed

    def start(self):
        self.last_file_check = self.log_file_stat()

        with open(self.log_path, 'r') as arq:
            if self.seek_previous_lines:
                arq.seek(0, os.SEEK_END)

            last_log_file_pointer = arq.tell()

            while True:
                if self.log_file_changed():
                    # print("LOG FILE CHANGED")
                    return last_log_file_pointer

                line = arq.readline()

                while '' != line:
                    last_log_file_pointer = arq.tell()
                    self.logs.append(line)

                    line = arq.readline()

                if len(self.logs) > 0 and len(self.logs[-1]) < 61:
                    arq.seek(last_log_file_pointer)

                if len(self.logs) > 0:
                    Sender(self.logs).start()
                    self.logs = []

                sleep(self.READ_FILE_FREQUECY_IN_SECONDS)
