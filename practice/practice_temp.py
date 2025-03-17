temp_argument = {
    "hello": "world",
    "name": "yjee",
    "age": 30
}


def print_argument(*args, **kwargs):
    print(args)
    print(kwargs)


print_argument(
    *temp_argument,
    **temp_argument
)


from decorator import *

# No.1
result = say_hello("yjee")
print(result)

# No.2
result = greet("yjee")
print(result)

# No.3
result = slow_function()
print(result)

# No.4
result = divide(10, 2)
print(result)

# No.5

# No.6

# No.7

# No.8

# No.9

# No.10
cal = Calculator()
result = cal.add(10, 20)
print(result)
result = cal.subtract(10, 20)
print(result)