def calculate(min, max, step):
    a2 = (min + step)
    a3 = (a2 + step)
    sum = min + a2 + a3
    if(a3 > max):
        print(min + a2)
    else:
        print(sum)

calculate(1, 3, 1)
calculate(4, 8, 2)
calculate(-1, 2, 2)