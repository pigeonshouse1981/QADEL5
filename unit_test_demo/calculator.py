class Calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def get_sum(self):
        return self.a + self.b

    def get_difference(self):
        return self.a - self.b

    def get_product(self):
        return self.a * self.b

    def get_quotient(self):
        return self.a / self.b

    def get_root(self):
        return self.a / self.b

myCalc = Calculator(a = 2, b = 5)

answer = myCalc.get_sum()
print (answer)