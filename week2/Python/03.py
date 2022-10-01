def func(a):
    def func2(b, c):
        print(a+b*c)
    return func2

func(2)(3, 4)
func(5)(1, -5)
func(-3)(2, 9)
