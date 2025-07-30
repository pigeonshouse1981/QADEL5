
import pandas as pd

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

    def times_table(self, multiplier, up_to=1048576):
        data = {
            "N": list(range(1, up_to + 1)),
            f"{multiplier} x N": [multiplier * i for i in range(1, up_to + 1)]
        }
        df = pd.DataFrame(data)
        print(df)

#answer = myCalc.get_sum()
#print (answer)