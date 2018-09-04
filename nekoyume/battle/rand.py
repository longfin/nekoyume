import random

class Random:
    def __init__(self, seed):
        self.seed(seed)

    def seed(self, value):
        random.seed(value)

    def randint(self, min, max):
        return random.randint(min, max)

    def shuffle(self, l):
        return random.shuffle(l)

class WeightedList:
    length = 0
    def __init__(self):
        self.values_ = []
        self.weights_ = []

    def __len__(self):
        return len(self.values_)

    def __str__(self):
        return str((self.values_, self.weights_))

    def add(self, value, weight):
        self.values_.append(value)
        self.weights_.append(weight)
        self.length = len(self.values_)
    
    def select(self, pop=False):
        if len(self.values_) == 0:
            return None
        weight_sum = 0
        for i in self.weights_:
            weight_sum += i
        rnd = random.randint(0, weight_sum - 1)
        idx = -1
        for i in range(len(self.values_)):
            if rnd < self.weights_[i]:
                idx = i
                break
            rnd -= self.weights_[i]
        if idx < 0:
            return None
        ret = self.values_[idx]
        if pop:
            del self.values_[i]
            del self.weights_[i]
        return ret

    def pop(self):
        return self.select(True)
