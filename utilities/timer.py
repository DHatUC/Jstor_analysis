from datetime import datetime


class Timer:

    def __init__(self, name):
        self.start_ts = datetime.now()
        self.name = name

    def ends(self):
        time_cost = datetime.now() - self.start_ts
        print('{} is finished. Time cost is {}'.format(self.name, time_cost))
