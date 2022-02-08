前两章我们了解了有限群和椭圆曲线，特别是了解了椭圆曲线上的点如何进行”加法“操作。有意思的是，如果我们将有限群里面的点与椭圆曲线结合起来能产生非常奇妙的化学反应。从上一节我们看到，如果二位平面上一个点如果在椭圆曲线上，那么我们把该点的x值放入椭圆曲线方程右边，也就是包含x变量的那边，然后把点的y坐标放入左边，也就是包含y变量的那部分，两边算出来的结果就会相等。

现在我们要定义有限群里面的点是否位于椭圆曲线上。从前面章节我们知道，有限群中点的”加法“和”乘法“是在普通加法和乘法基础上进行求余运算后所得的结果。我们把求余操作带入到椭圆曲线上，如果一个有限群中的点，把它的x和y带入到椭圆曲线方程，先计算对应结果，然后再进行求余运算，如果求余后结果相同，那么我们就说该点在椭圆曲线上。

例如给定椭圆曲线方程：y ** 2 = x ** 3 + 7, 然后给定有限群F(103)中的一点(17, 64)，这个点就在给定椭圆曲线上，因为将改点的x带入右边进行求余运算：
(17 ** 3 + 7) % 103 = 79
把y带入左边进行求余运算：
(64 ** 2) % 103 = 79
左右两边在求余运算后相同，所以根据定义，该点就在椭圆曲线上。上一节我们详细说明了如何对椭圆曲线上两点进行“加法”操作，其本质是先找到两点形成的直线，根据直线与曲线相交的情况计算第三点，在计算过程中我们进行了很多加减乘除运算，现在我们只要把上一节运算的过程加上求余，我们就能将有限群中的点与椭圆曲线结合起来。

上一节我们实现椭圆曲线时，传入的是普通的整形数值，现在我们传入前面定义的有限群元素，由于我们重载了元素的运算操作，因此我们可以用有限群元素直接替换整形数，例子如下：
```
a = FieldElemet(0, 223)
b = FieldElemet(7, 223)
x = FieldElemet(192, 223)
y = FieldElemet(105, 223)

p = EllipticPoint(x, y, a, b)
```
上面代码运行后结果如下：
```
p + p is :x:FieldElement with value:49 and order:223, y:FieldElement with value:71 and order:223, a:FieldElement with value:0 and order:223, b:FieldElement with value:7 and order:223
```
为何有限群跟椭圆曲线在一起能实现加密效果呢，那是因为有限群元素如果位于给定的椭圆曲线上，它经过“加法”运算后所得结果非常随机。也就是如果你拿到一个结果，在理论上你无法反推出到底是哪两个有限群元素”相加“。我们以最简单的直线方程为例：y = ax + b，然后将有限群元素带入，所得结果类似如下情况：
![请添加图片描述](https://img-blog.csdnimg.cn/205cb1ca726a4cb0a5738ff0a6d464a2.png)
你会看到结果的分布非常随机，找不到任何规律，这种无法从结果逆推回原因的计算过程最适合用来做加密，从上图看到有限群元素在简单的直线上进行相应计算结果都这么随机，在椭圆曲线上那就更随机了。

我们前面定义了椭圆曲线上点的加法操作，但是还没有定义元素与一个常量的乘法操作，其实乘法不过就是将加法重复给定次数，给定椭圆曲线上一个点G，然后它不断给自己做“加法”操作，重复自己“加”自己一定次数后，我们会得到前面定义的“零点”，假设G经过n次自加后得到椭圆曲线上的零点，由此形成n个椭圆曲线点形成的集合：
{G, 2G, 3G, ..., nG} 
我们用“组”来形容它，椭圆曲线上的点做数值乘机很容易，但反过来给定一个点，让你查找它是哪个点和哪个常量的乘积则非常困难，这个特性决定了椭圆曲线的加密功能。下面我们看看如何实现椭圆曲线上点的常量乘积，代码如下：
```
    def __rmul__(self, scalar):
        result = self.__class__(None, None, self.a, self.b)
        for i in range(scalar):
            result += self
        return result
```
代码很简单，本质上就是将乘积转换成多次加法。我们测试一下上面代码：
```
x = FieldElemet(47,  223)
y = FieldElemet(71, 223)
p = EllipticPoint(x, y, a, b)
for s in range(1, 21):
    result = s * p
    print(f"{s} * [(47,71) over 233]  = [({result.x.num},{result.y.num}) over 233]")
```
上面代码运行后输出结果如下：
```
1 * [(47,71) over 233]  = [(47,71) over 233]
2 * [(47,71) over 233]  = [(36,111) over 233]
3 * [(47,71) over 233]  = [(15,137) over 233]
4 * [(47,71) over 233]  = [(194,51) over 233]
5 * [(47,71) over 233]  = [(126,96) over 233]
6 * [(47,71) over 233]  = [(139,137) over 233]
7 * [(47,71) over 233]  = [(92,47) over 233]
8 * [(47,71) over 233]  = [(116,55) over 233]
9 * [(47,71) over 233]  = [(69,86) over 233]
10 * [(47,71) over 233]  = [(154,150) over 233]
11 * [(47,71) over 233]  = [(154,73) over 233]
12 * [(47,71) over 233]  = [(69,137) over 233]
13 * [(47,71) over 233]  = [(116,168) over 233]
14 * [(47,71) over 233]  = [(92,176) over 233]
15 * [(47,71) over 233]  = [(139,86) over 233]
16 * [(47,71) over 233]  = [(126,127) over 233]
17 * [(47,71) over 233]  = [(194,172) over 233]
18 * [(47,71) over 233]  = [(15,86) over 233]
19 * [(47,71) over 233]  = [(36,112) over 233]
20 * [(47,71) over 233]  = [(47,152) over 233]
```
从输出结果可以看到随机性很强，在数学上给定点(139,86),你要逆向得到它是(47, 71)与常量15相乘，这几乎是不可能的。上面提到的“组”这个数学概念与前面提到的"群“一大区别在于，它只有”加法“，没有对应”乘法“，对于“组”而言，它有几个性质，第一，它一定包含一个“零点”，其实只要我们将位于椭圆曲线上的有限群中的一个点，让它不断自加，加到一定次数后就能实现我们上一节所描述的“零点”。 第二个是封闭性，也就是“组”内任意两个元素相加，所得结果也在“组”内，例如一个元素为a\*G, 另一个为b\*G, 相加后所得结果为(a+b)\*G，它依然是点G与一个常量相乘的结果。

第三个特性是相反性，也就是对任意一个“组”中元素a,在“组”里必然存在另一个元素b,使得a+b=0。第四是交换性，也就是a + b = b + a。第五是结合性，A+(B+C) = (A+B)+C。假设点G经过n次自加后得到“零点”，那么n就称为”组“的规模。

假设我们有椭圆曲线为y^2 = x^3 + 7, 对应的有限群为{0,1,2...,222}，其中(15,86)是有限群中的一点，并且在曲线上，我们看看它生成的群的规模有多大：
```

p = EllipticPoint(x, y, a, b)
p1 = p + p
n = 1
while p1 != p:
    p1 += p
    n += 1

print(f"order of the group is {n}")
```
上面代码运行结果为n:
order of the group is 7
也就是说元素(15, 86)在椭圆曲线上所生成的“组”的规模为7.
我们需要改进一下常量乘法的实现，我们现在做的是将加法操作重复给定次数，但如果常量数值很大，例如壹万亿，那么当前做法效率会非常低效，我们采用一种叫"binary expansion“的方法，实现如下：
```
 def __rmul__(self, scalar):
        result = self.__class__(None, None, self.a, self.b)
        current = self
        while scalar:
            if scalar & 1:
                result += current
            current += current
            scalar >>= 1
        return result
```
它的逻辑很不难理解，它先把若干次加法的结果攒起来，然后再一次性加过去，例如要执行二十次相加，那么我们先积攒十次相加的结果，然后把积攒的的结果相加即可。

要让椭圆曲线形成公钥加密系统，我们需要确定以下信息：
1，确定椭圆曲线多项式中的参数a,b
2，确定有限群元素的个数
3，确定用于生成”组“的元素G
4，确定”组“的规模n

对于比特币使用的相关参数如下：
1， a = 0, b = 7,
2, p = 2^256  - 2 ^ 32 - 977
3， Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
4， Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
5,  n  =  0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
同时比特币的椭圆曲线函数也称为secp256k1。

从p 和 n的设置看，有限群中的元素其规模都在64字节，在这样的数量级下，没有任何算力能对加密结果进行破解。现在我们修改有限群的实现，让它契合比特币的特性：
```
P = 2 ** 256 - 2 ** 32 - 977
class BitcoinFieldElement(FieldElemet):
    def __init__(self, num, prime = None):
        super().__init__(num, P)
    def __repr__(self):
        return "{:x}".format(self.num).zfill(64)  # 填满64个数字
```
同理我们定义用于比特币的椭圆曲线：
```
A = 0
B = 7
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141


class BitcoinEllipticPoint(EllipticPoint):
    def __init__(self, x, y, a = None, b = None):
        a, b = BitcoinFieldElement(A), BitcoinFieldElement(B)
        if type(x) == int:
            super().__init__(x = BitcoinFieldElement(x), y = BitcoinFieldElement(y), a = a, b = b)
        else:
            super().__init__(x = x, y = y, a = a, b = b)

    def __rmul__(self, scalar):
        scalar = scalar % N
        return super().__rmul__(scalar)
```
我们看看上面代码运行的结果：
```

G = BitcoinEllipticPoint(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
                         0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
print(N * G)
```
我们定义了生成点，然后设置了”组“的规模N，用它乘以生成点，预期结果应该是0，代码运行后输出如下：
```
x:None, y:None, a:0000000000000000000000000000000000000000000000000000000000000000, b:0000000000000000000000000000000000000000000000000000000000000007
```
可以看到，输出的确实是椭圆曲线上定义的”零点“.由此我们可以实现椭圆曲线加密，假设给定一个秘钥e, 加密就是P = eG，有了e 和 G，计算P很容易，但是有了P，在理论上无法推导出e。下面我们看看如何使用椭圆曲线实现数字签名。

数字签名目的就是为了验证给定信息属于特定人。首先我们每个人先获取一个秘钥e,这个秘钥就像我们的身份证那样不能丢失，一旦丢失本人的身份就会被他人冒充。假设我发出一条消息z="我请大家吃饭”，收到这条消息的人怎么确认这句话的确是我说的，而不是别有用心的人冒充我说的呢，一个办法是我把秘钥e和消息z合在一起发出去，但这样相当于我的身份证被暴露，以后别人就可以拿到e，然后用同样的方法来冒充我，因此我不能把e暴露出来。

还有一种解决办法是，我根据发出的不同消息，使用e来创建一个相对应的数据s，而且在数学上可以证明，只有拥有e的人才能构造s，这样我就可以在不暴露e的情况下，别人拿到消息内容和数值s，通过特定的计算方法后确定我的确是拥有e的那个人，我们看看怎么构造这个数值s。注意在这里s, z, e都是256比特位的数字，这里你可能会疑问，z不是对应一个字符串或者是文本信息吗，怎么变成256比特位的数值呢，其实很简单，我们将文本或字符串进行一次sha256哈希计算即可。

第一步，我们计算 P = eG，也就是用数值e跟椭圆曲线上点G做常量乘法，得到曲线上的另一点P，注意到P是一个二维平面上的点，它有x,y两个坐标，这里我们只使用它的x坐标，假设R在x坐标上对应的值为r。

第二步，我们选取一个256位，也就是32字节长度的随机数k, 计算R = kG。显然R也是椭圆曲线上的一点。

第三步，我们需要构造两个数值u, v，他们不等于0，但是能满足uG + vP = R。现在问题在于，如何构造u, v。其实这两个数值是多少并不重要，它们的作用在于逻辑推导上。首先我们把式子展开，也就是uG + vP = R => uG + v(eG) = kG, 左右两步消去G就有 u + ve = k 

第四步，我们需要找到一个特定的数值s，使得u = z / s，v = r / s,注意虽然e, s, u, v, k 这些都是256位的整形数，但同时它们也都属于比特币所定义的有限群中的元素，注意比特币有限群的元素就是{0,1, ... P -1}，因此他们进行的运算都对应我们前面描述的有限群元素的操作，因此 u / s并不是将数值u简单的对s进行除法，而是让u 乘以 s对应的逆元素，r / s也同理，前面我们也详细描述过如何通过费马小定理来计算给定元素的逆元素。

当然这里还有一个问题，我们现在还不知道u的具体值，那么怎么计算u / s呢。其实我们不需要知道u的值就能确定s 。首先假设我们已经有了s的值，那么将 u = z / s, v = r / s代入 u + ve = k就有 z / s + e(r/s) = k, 于是有s = (z + e * r ) / k，由于z, e, r, k都已知，于是s就计算了出来，注意这里的加法，乘法，除法都是针对有限群元素的操作，而不是普通的四则运算，因此s是一个整数，也是有限群里面的一个元素。

第五步，我将(s, r, z, P)公布出来，别人就可以利用s, r来验证z确实是我发出来的信息，验证过程其实很简单，对方先计算u =  z / s,  v = r / s, 然后计算u * G + v  * P , 如果算出来的结果对应的x坐标值正好等于r，那么签名就可以认证通过。

算法成立的根本原因在于，s 和 e 在数学上是一一对应的关系，只有拥有e的人才能生成s，因此一旦对方验证了s后就能确认我是拥有e的人。这里还需注意的是，我们除了不能泄露e，同时也不能泄露随机数k，如果k泄露了，e也会被计算出来，同时也要注意，我们要根据不同的消息生成不同的k，这样才能保证k不被对方通过统计等方式破解出来。

我们看看如何在代码上实现签名认证逻辑：
```
def verify_signature(r, s, z, P):
    s_invert = pow(s, N - 2, N)  # 使用费马小定理直接找到s的逆元素
    u = z * s_invert % N  # u = z / s
    v = r * s_invert % N # v = r / s
    return (u * G + v * P).x.num == r # 检验x坐标对应数值是否等于 r
```
接下来我们给定z, s, r, P 的值，然后运行上面认证代码看看结果：
```
z = 0xec208baa0fc1c19f708a9ca96fdeff3ac3f230bb4a7ba4aede4942ad003c0f60
r = 0xac8d1c87e51d0d441be8b3dd5b05c8795b48875dffe00b7ffcfac23010d3a395
s = 0x68342ceff8935ededd102dd876ffd6ba72d6a427a3edb13d26eb0781cb423c4

verify_res = verify_signature(r = r, s = s, z = z, P = P)
print(f"verify result is {verify_res}")
```
上面代码运行后所得结果为：
```
verify result is True
```
我们把上面逻辑封装一下以便以后使用：
```
class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s
    def __repr__(self):
        return f"Signature({self.r}, {self.s})"
```
接着我们把verify_signature的逻辑挪到BitcoinEllipticPoint：
```
 def verify(self, z, sig):
        s_invert = pow(sig.s, N- 2, N) #费马小定理计算s的逆
        u = z * s_invert % N
        v = sig.r * s_invert % N
        total = u * G + v * self
        return total.x.num == sig.r
```
现在我们可以看看椭圆曲线签名的流程，它的步骤如下：
1， 先把要认证的文本经过sha256哈希成256比特位的数值，利用我们的秘钥计算sG = P
2，选择一个随机整数k，计算R = kG, 然后取出R的x坐标对应的值，我们用r来记录
3，计算s = (z + r * e) / k 注意这里的运算都是针对有限群元素的操作。
4，将(r, s)发布出来作为自己的签名

我们看看签名流程的实现：
```

private_key_str = "this is my secret key"
message_str = "message I want to send"
e = "0x" + hashlib.sha256(private_key_str.encode('utf-8')).hexdigest()
z = "0x" + hashlib.sha256(message_str.encode('utf-8')).hexdigest()
k = randrange(10000)

r = (k * G).x.num
k_invert = pow(k, N - 2, N) #费马小定理计算k的逆


e = int(e, 16) #将字符串转换为数字
z = int(z, 16)
P = e * G #这个是公钥，需要用于验证签名
s = (z + r * e) * k_invert % N

print(f"r is {hex(r)}")
print(f"s is {hex(s)}")
print(f"public key is: {P}")
```
上面代码运行后结果如下：
```
r is 0x727ca544e2d65a174911edd94e5c3490a2b087ff32c0e4b42c7e37f964d082a8
s is 0xd4b49c0267834c6cf4b7ebcad81720544ccdb06c8bd9bcd81cf48d366070b96b
public key is: x:0e3fe875c860168d342caadc3a0688ad40fd96bf5620ad3bedacfb640da61046, 
y:5bb7ede8cdef2260eb9d832b3180b7f7e5bd6da23b1f10cd965601ceda482150, 
a:0000000000000000000000000000000000000000000000000000000000000000, 
b:0000000000000000000000000000000000000000000000000000000000000007

```
我们把上面签名过程的逻辑封装一下：
```
class PrivateKey:
    def __init__(self, secret):
        self.secret = secret
        self.point = secret * G

    def hex(self):
        return "{:x}".format(self.secret).zfill(64)

    def sign(self, z):
        k = randrange(N)
        r = (k * G).x.num
        k_invert = pow(k, N - 2, N)
        s = (z + r * self.secret) * k_invert % N
        if s > N / 2:
            s = N - s
        return Signature(r, s)

pk = PrivateKey(e)
sign = pk.sign(z)
print(sign)
```
我们需要非常注意的是，椭圆曲线在每次签名时，必须确保k是不同的随机数，不然秘钥e会被破解出来。由此衍生出一个名为RFC6979的标准，专门用于生成k，他的实现如下：
```

    def deterministic_k(self, z):
        k = b'\x00' * 32
        v = b'\x01' * 32
        if z > N:
            z -= N
        z_bytes = z.to_bytes(32, 'big')
        secret_bytes = self.secret.to_bytes(32, 'big')
        s256 = hashlib.sha256
        k = hmac.new(k, v + b'\x00' + secret_bytes + z_bytes, s256).hexdigest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b'\0x1' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            candidate = int.from_bytes(v, 'big')
            if candidate >= 1 and candidate < N:
                return candidate
            k = hmac.new(k ,v + b'\x00', s256).digest()
            v = hmac.new(k, v, s256).digest()
```
上面的逻辑我们不需要关心，只要知道经过上面处理过的k足够随机就行。在区块链应用中，有很大一部工程性问题就是如何将这些数据结构进行序列化然后放到网络上穿来穿去，因此序列化将是下一节要点。


