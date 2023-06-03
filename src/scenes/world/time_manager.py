from engine.time import Time

days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


class TimeManager:
    current_time_minutes = 360
    time_speed_factor = 1.4
    current_day_of_week = 0
    day_ended = False
    day_close_to_end = False

    @classmethod
    def formatted_time(cls) -> str:
        hours = int(cls.current_time_minutes / 60)
        minutes = (int(cls.current_time_minutes % 60) // 10) * 10
        time_string = "{:02d}:{:02d}".format(hours, minutes)
        return time_string

    @classmethod
    def formatted_week_day(cls) -> str:
        return days[cls.current_day_of_week]

    @classmethod
    def restart(cls):
        cls.day_ended = False
        cls.current_time_minutes = 360
        cls.current_day_of_week += 1
        if cls.current_day_of_week > 6:
            cls.current_day_of_week = 0

    @classmethod
    def update(cls) -> None:
        if cls.day_ended:
            return
        cls.current_time_minutes += cls.time_speed_factor * Time.dt
        # Tells if the day is close to end
        if not cls.day_close_to_end and cls.current_time_minutes >= 1000:
            cls.day_close_to_end = True
        # Tells if the day is ended
        if cls.current_time_minutes >= 1320:
            cls.day_ended = True
