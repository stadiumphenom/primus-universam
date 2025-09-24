import random

class EnergyPulse:
    """
    Models the 3-6-9 harmonic energy system.
    Provides a stable `.energy` property so UIs can track energy state.
    """

    def __init__(self, starting_energy: int = 100):
        # total available energy
        self.level = starting_energy
        # history of energy usage
        self.history = []

    @property
    def energy(self) -> int:
        """Expose current energy level as a property."""
        return self.level

    def pulse(self) -> int:
        """
        Perform one energy pulse.
        Returns the energy cost consumed.
        """
        # consume random harmonic amount (3, 6, or 9)
        cost = random.choice([3, 6, 9])
        if self.level - cost < 0:
            cost = self.level  # don't go below 0
        self.level -= cost
        self.history.append(cost)
        return cost

    def recharge(self, amount: int = 10) -> None:
        """Recharge energy by a given amount."""
        self.level += amount

    def reset(self, value: int = 100) -> None:
        """Reset to starting value."""
        self.level = value
        self.history.clear()
