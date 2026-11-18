class Calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
        self.bren = 2.5

    def get_sum(self):
        return self.a + self.b
    
    def get_multiply(self):
        return self.a * self.b
    
    def get_subtract(self):
        return self.a - self.b

    def get_divide(self):
        return self.a / self.b
    
if __name__ == "__main__":
    mycalc = Calculator(a=5,b=6)
    print(mycalc.get_sum())