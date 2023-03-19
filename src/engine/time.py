import pygame

# ---------- Time ----------
dt = 0.2
clock = pygame.time.Clock()


def update():
    """
    Update time on the event loop, and calculates delta time.
    """
    global dt, clock
    dt = clock.tick() / 1000


class Timer:
    """
    Timer that counts down from a specified duration in seconds.
    """

    def __init__(self, duration_seconds: int):
        """
        Initializes a new Timer object.
        :param duration_seconds: The duration of the timer in seconds.
        """
        self.starting_time: int = None
        self.duration = duration_seconds * 1000
        self._started = False

    def start(self):
        """
        Starts the timer.
        """
        self._started = True
        self.starting_time = pygame.time.get_ticks()

    def update(self) -> bool:
        """
        Updates the timer and returns True if the timer has completed.
        :return: True if the timer has completed, otherwise False.
        """
        if not self._started:
            return False
        if pygame.time.get_ticks() - self.starting_time > self.duration:
            self._started = False
            return True
        return False
