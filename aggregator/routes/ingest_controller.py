from routes import app, request
from datetime import datetime, timedelta
import logging


class Singleton:

    _instance = None

    def __init__(self):
        self.realtime_audience = {}
        self.realtime_audience_count = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def process(self, data):
        for local_time in data:
            if not local_time in self.realtime_audience:
                self.realtime_audience[local_time] = {}
                self.realtime_audience_count[local_time] = {}

            for transmission_id in data[local_time]:
                if not transmission_id in self.realtime_audience[local_time]:
                    self.realtime_audience[local_time][transmission_id] = {}
                    self.realtime_audience_count[local_time][transmission_id] = 0

                for audience_id in data[local_time][transmission_id]:
                    if not audience_id in self.realtime_audience[local_time][transmission_id]:
                        self.realtime_audience[local_time][transmission_id][audience_id] = \
                            data[local_time][transmission_id][audience_id]
                        self.realtime_audience_count[local_time][transmission_id] =  \
                            self.realtime_audience_count[local_time][transmission_id] + 1

    def get_state(self, transmission_id):
        ref_date = (datetime.now() - timedelta(minutes=2)
                    ).strftime("%d/%b/%Y:%H:%M")

        del_date = (datetime.now() - timedelta(minutes=3)
                    ).strftime("%d/%b/%Y:%H:%M")

        if del_date in self.realtime_audience:
            del self.realtime_audience[del_date]
            del self.realtime_audience_count[del_date]

        logging.debug(ref_date)

        if ref_date in self.realtime_audience:
            if transmission_id in self.realtime_audience[ref_date]:
                return self.realtime_audience_count[ref_date][transmission_id]
            else:
                return 0
        else:
            return 0


@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.get_json()
    # logging.warn(data)
    Singleton.instance().process(data)

    return 'ok'


@app.route('/get_state/<transmission_id>', methods=['GET'])
def get_state(transmission_id):
    return str(Singleton.instance().get_state(transmission_id))
