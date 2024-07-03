import random

number_set = [
        2, 5, 8, 11, 14, 17, 20, 22, 24, 27, 30, 33, 36, 39, 42, 45, 47, 49,
        52, 55, 58, 61, 64, 67, 70, 72, 74, 77, 80, 83, 85, 87, 90, 93, 96, 98, 100
    ]

def get_median(numbers):
    n = len(numbers)
    if n % 2 == 1:
        return numbers[n // 2]
    else:
        return random.choice([numbers[n // 2 - 1], numbers[n // 2]])

class Bot:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.number = self.generate_number()
        self.upper_end = 100
        self.lower_end = 1
        self.optimized_counterattack = False

    def generate_number(self):
        return random.randint(1, 100)

    def guess(self):
        return random.randint(self.lower_end, self.upper_end)

    def reset_number(self):
        self.number = random.randint(1, 100)

    def reset_bounds(self):
        self.upper_end = 100
        self.lower_end = 1

# bot optimized for offense
class BotOffense(Bot):
    def guess(self):
        return int((self.lower_end + self.upper_end) / 2)  # binary search

# bot optimized for defense
class BotDefense(Bot):
    def generate_number(self):
        return random.choice(number_set)

# bot optimized for offense and defense
class BotOptimized(BotOffense):
    def generate_number(self):
        return random.choice(number_set)

# bot that can counter the optimized bot
class BotOptimizedCounterattack(BotOptimized):
    def __init__(self, name):
        super().__init__(name)
        self.number_set = [
            2, 5, 8, 11, 14, 17, 20, 22, 24, 27, 30, 33, 36, 39, 42, 45, 47, 49,
            52, 55, 58, 61, 64, 67, 70, 72, 74, 77, 80, 83, 85, 87, 90, 93, 96, 98, 100
        ]
        self.optimized_counterattack = True
        self.last_guess = None

    def guess(self):
        self.last_guess = get_median(self.number_set)
        return self.last_guess

    def reset_bounds(self):
        self.number_set = [
            2, 5, 8, 11, 14, 17, 20, 22, 24, 27, 30, 33, 36, 39, 42, 45, 47, 49,
            52, 55, 58, 61, 64, 67, 70, 72, 74, 77, 80, 83, 85, 87, 90, 93, 96, 98, 100
        ]
