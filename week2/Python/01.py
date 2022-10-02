def calculate(min, max, step):
    sum = 0
    while min <= max:
        sum = sum + min
        min = min + step
    print(sum)


calculate(1, 3, 1)
calculate(4, 8, 2)
calculate(-1, 2, 2)