class Person():
    first = "Robert"

    def __init__(self, last):
        self.last = last

    def greet(self):
        print('I am {} {}'.format(self.first, self.last))

if __name__ == "__main__":
    a = Person("Dominguez")
    a.greet()