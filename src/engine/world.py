import src.engine.time as game_time
from enum import Enum


class WeekDays(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class World:
    def __init__(self):
        self.day_time = 1100
        self.day_speed = 1.4
        self.week_day = 0

    def time_string(self):
        hours = int(self.day_time / 60)
        minutes = (int(self.day_time % 60) // 10) * 10
        time_string = "{:02d}:{:02d}".format(hours, minutes)
        return time_string

    def update(self):
        self.day_time += self.day_speed * game_time.dt

        if self.day_time >= 1320:
            self.day_time = 360
            self.week_day += 1
            if self.week_day > 6:
                self.week_day = 0


instance = World()
