from engine.time import Time


class TimeManager:
    current_time_minutes = 1180
    time_speed_factor = 1.4
    current_day_of_week = 0

    @classmethod
    def formatted_time(cls) -> str:
        hours = int(cls.current_time_minutes / 60)
        minutes = (int(cls.current_time_minutes % 60) // 10) * 10
        time_string = "{:02d}:{:02d}".format(hours, minutes)
        return time_string

    @classmethod
    def update(cls) -> None:
        cls.current_time_minutes += cls.time_speed_factor * Time.dt
        if cls.current_time_minutes >= 1320:
            cls.current_time_minutes = 360
            cls.current_day_of_week += 1
            if cls.current_day_of_week > 6:
                cls.current_day_of_week = 0
