class Available:
    def __init__(self, time=None, location=None):
        """
        :param time:
        For students:
        {
            "MON": [{"start": Time, "end": Time}, ..., {"start": Time, "end": Time}],
            ...,  # TUE - FRI
            "SUN": [{"start": Time, "end": Time}, ..., {"start": Time, "end": Time}]
        }
        For internships:
        [
            # options
            {
                "MON": [{"start": Time, "end": Time}, ..., {"start": Time, "end": Time}],
                ...,  # TUE - FRI
                "SUN": [{"start": Time, "end": Time}, ..., {"start": Time, "end": Time}]
            },
            ...,
            {
                "MON": [{"start": Time, "end": Time}, ..., {"start": Time, "end": Time}],
                ...,  # TUE - FRI
                "SUN": [{"start": Time, "end": Time}, ..., {"start": Time, "end": Time}]
            }
        ]
        :param location:
        """
        self.time = time
        self.location = location

    def time_flex(self):
        return self.time is None

    def location_flex(self):
        return self.location is None

    def match_location(self, internship):
        if self.location_flex():
            return 1
        if internship.location_flex():
            return 0
        # both flexible location
        return 1 if self.location == internship.location else 0

    def match_time(self, internship):
        if self.time_flex():
            return 1
        if internship.time_flex():
            return 0
        # both flexible time
        return self.time[0]

    def match(self, internship):
        return self.match_time(internship) * self.match_location(internship)


def get_day(week, day_name):
    day = week.get(day_name, [])
    if type(day) is list:
        day = get_day(week, day)
    return day


def intersect_week(week1, week2):
    total = 0
    for day_name in ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']:
        total += intersect_day(get_day(week1, day_name), get_day(week2, day_name))


def intersect_day(day1, day2):
    total = 0
    i = j = 0
    len1, len2 = len(day1), len(day2)
    while i < len1 and j < len2:
        hours, remain = intersect(day1[i], day2[j])
        total += hours
        if remain == 1:
            j += 1
        elif remain == 2:
            i += 1
        elif remain is None:
            i += 1
            j += 1
    return total


def intersect(period1, period2):
    hours = max(min(period1[1], period2[1]) - max(period1[0], period2[0]), 0)
    remain = None if period1[1] == period2[1] else (1 if period1[1] > period2[1] else 2)
    return hours, remain
