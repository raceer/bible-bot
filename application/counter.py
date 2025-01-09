class Counter:
    def __init__(self, default_value = 0, previous_value = 0):
        self.default_value = default_value
        self.counter = previous_value 

    def retrieve_value(self):
        self.counter += 1
        return self.counter - 1

    def reset_counter(self):
        self.counter = self.default_value

if __name__ == "__main__":
    count = Counter()
    print(count.retrieve_value())
    print(count.retrieve_value())
