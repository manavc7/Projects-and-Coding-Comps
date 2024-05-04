def camelsnakeconverter(camel):
    snake = camel[0]
    for i in camel[1:]:
        if i.isupper():
            snake += "_" + i.lower()
        else:
            snake += i
    snake = snake.lower()

    return snake



camel = input("camel case: ")
print("snake case: " + camelsnakeconverter(camel))


