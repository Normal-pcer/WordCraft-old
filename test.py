class a:
    @staticmethod
    def f():
        return 5

    b: list


a.b = [[a.f() for j in range(16)] for i in range(16)]

print(a.b)
