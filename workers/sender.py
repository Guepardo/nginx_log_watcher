from threading import Thread
from time import sleep
from urlparse import parse_qs


class Sender(Thread):
    def __init__(self, logs=[]):
        Thread.__init__(self)
        self.logs = logs

    def run(self):
        print("sending.....")
        print("BATCH SIZE %d" % len(self.logs))

        data = {}
        for log in self.logs:
            time, _, raw_querystring, _, _ = log.split(',')

            time = time[0:17]
            querystring = parse_qs(raw_querystring)

            transmission_id = querystring[' transmission_id'][0]
            audience_id = querystring['audience_id'][0]

            if not time in data:
                data[time] = {}

            if not transmission_id in data[time]:
                data[time][transmission_id] = {}

            audience_data = {
                "arg1": querystring['arg1'][0],
                "arg2": querystring['arg2'][0]
            }

            data[time][transmission_id][audience_id] = audience_data

        print("LAST LINE [%s]" % self.logs[0])
        print(data)
        print("--------")
