class Counter:
    def __main__(self):
        self.default_value = 0
        self.counter = self.default_value

    def retrieve_value(self):
        self.counter += 1
        return self.counter - 1

    def reset_counter(self):
        self.counter = self.default_value