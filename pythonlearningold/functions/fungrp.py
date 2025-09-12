def func1():
    pass


def func2(x):  # x = 3
    print("This is my variables:", x)


def func3(x=5, y=6):  # x = 3, y = 4
    print("This is my variables:", x, y)
    sum = x + y
    print("Sum of x and y is:", sum)


def func4(**kwargs):
    print("This is my variables:", kwargs)


def func5(*args):
    print("This is my variables:", args)


def func6(x, y):
    print("This is my variables:", x, y)
    sum = x + y
    print("Sum of x and y is:", sum)


def func7(x, y):
    print("This is my variables:", x, y)
    sub = x - y
    print("Sub of x and y is:", sub)


def func8(x, y):
    print("This is my variables:", x, y)
    mul = x * y
    print("Multiplication of x and y is:", mul)
    div = x / y
    print("Division of x and y is:", div)


# func6(3, 4)
# func7(10, 5)
# func8(6, 2)
