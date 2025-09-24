import itertools

class EnergyPulse:
    def __init__(self):
        self.sequence = itertools.cycle([3, 6, 9])

    def next_pulse(self):
        return next(self.sequence)
