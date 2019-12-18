class classA:

    def __init__(self, x, y):
        self.a = x
        self.b = y

    def changeA(self, x):
        self.a = x

    def __str__(self):
        return(f'a: {self.a}, b: {self.b}')


class classB:

    def __init__(self, x, y):
        self.y = classA(x, y)

    def newY(self, x):
        self.y = classA(x, x)

    def changeYa(self, x):
        self.y.changeA(x)

    def __str__(self):
        return(f'a: {self.y.a}, b: {self.y.b}')


foo = classB(1, 1)
print(foo)
foo.newY(2)
print(foo)
foo.changeYa(3)
print(foo)
