class FieldElemet:
    def __init__(self, num, prime):
        # prime 对应群的大小，也就是元素的数量, num就是元素对应数值
        if num >= prime or num < 0:
            # 群元素必须是大于等于0的整数
            error = f'field element shound be integer in range 0 to {prime-1}'
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return f'FieldElement with value:{self.num} and order:{self.prime}'

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError('there are two different field')
        num = (self.num + other.num) % self.prime
        #新建生成一个对象
        return self.__class__(num, self.prime)
    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError('there are two different fields')
        num = (self. num - other.num) % self.prime
        return self.__class__(num, self.prime)

    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError('there are two different fields')
        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)

    def __pow__(self, num):
        num = num % self.prime
        num = pow(self.num, num, self.prime)
        return self.__class__(num, self.prime)

    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError('there are two different fields')
        num = (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
        return self.__class__(num, self.prime)

    def  __rmul__(self, other): #实现元素与常量相乘
        num = (self.num * other) % self.prime
        return self.__class__(num, self.prime)



a = FieldElemet(7, 23)
b = FieldElemet(9, 23)
print(a - b)
print(a * b)

c = FieldElemet(3, 13)
d = FieldElemet(1, 13)
print(c ** 3 == d)

print(pow(4, 12, 13))

#F(13)的群元素
n = 5
field_before = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
field_after = []
for i in field_before:
    field_after.append((i * n) % 13)
print("field_after: ", field_after)

e = FieldElemet(12, 23)
f = FieldElemet(20, 23)
print( e / f)

print((20 * 19) % 23)

P = 2 ** 256 - 2 ** 32 - 977
class BitcoinFieldElement(FieldElemet):
    def __init__(self, num, prime = None):
        super().__init__(num, P)
    def __repr__(self):
        return "{:x}".format(self.num).zfill(64)  # 填满64个数字