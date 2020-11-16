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
        [city name, USA]
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
        score = 0
        for schedule in internship.time:
            total_time = total_time_in_week(schedule)
            if total_time == 0:
                continue
            score = max(score, intersect_week(self.time, schedule) / total_time)
        assert 0 <= score <= 1
        return score

    def match(self, internship):
        return self.match_time(internship) * self.match_location(internship)


def get_day(week, day_name):
    day = week.get(day_name, [])
    if type(day) is list:
        day = get_day(week, day)
    return day


def total_time_in_week(week):
    total = 0
    for day_name in week:
        total += total_time_in_day(week[day_name])
    return total


def total_time_in_day(day):
    total = 0
    for period in day:
        total += (period["end"].minutes - period["start"].minutes)
    return total


def intersect_week(week1, week2):
    total = 0
    for day_name in ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']:
        total += intersect_day(get_day(week1, day_name), get_day(week2, day_name))
    return total


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
    p1_s, p1_e, p2_s, p2_e = period1["start"].minutes, period1["end"].minutes, period2["start"].minutes, period2["end"].minutes
    minutes = max(min(p1_e, p2_e) - max(p1_s, p2_s), 0)
    remain = None if p1_e == p2_e else (1 if p1_e > p2_e else 2)
    return minutes, remain
