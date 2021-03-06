class Time:
    def __init__(self, time_str="0:0"):
        self.hour, self.minute = map(int, time_str.split(':'))

    def minutes(self):
        return self.hour * 60 + self.minute
