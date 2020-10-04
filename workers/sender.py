from threading import Thread
from time import sleep


class Sender(Thread):
    def __init__(self, logs=[]):
        Thread.__init__(self)
        self.logs = logs

    def run(self):
        print "wainting loog parse"
        sleep(6)
        print self.logs
        print "sending....."
