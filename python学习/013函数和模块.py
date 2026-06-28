# 定义函数
# 输入m和n，计算组合数C(m,n)的值
# 通过关键字def定义求阶乘的函数
# 自变量（参数）num是一个非负整数
# 因变量（返回值）是num的阶乘
def fac(num):
    result = 1
    for n in range(2, num + 1):
        result *= n
    return result


m = int(input('m = '))
n = int(input('n = '))
# 计算阶乘的时候不需要写重复的代码而是直接调用函数
# 调用函数的语法是在函数名后面跟上圆括号并传入参数
print(fac(m) // fac(n) // fac(m - n))

# 输入m和n，计算组合数C(m,n)的值
from math import factorial

m = int(input('m = '))
n = int(input('n = '))
print(factorial(m) // factorial(n) // factorial(m - n))

# 输入m和n，计算组合数C(m,n)的值
from math import factorial as f

m = int(input('m = '))
n = int(input('n = '))
print(f(m) // f(n) // f(m - n))


# 函数的参数
# 位置参数和关键字参数
def make_judgement(a, b, c):
    """判断三条边的长度能否构成三角形"""
    return a + b > c and b + c > a and a + c > b
# 上面make_judgement函数有三个参数，这种参数叫做位置参数，在调用函数时通常按照从左到右的顺序依次传入，而且传入参数的数量必须和定义函数时参数的数量相同，如下所示。
print(make_judgement(1, 2, 3))  # False
print(make_judgement(4, 5, 6))  # True
print(make_judgement(b=2, c=3, a=1))  # False
print(make_judgement(c=6, b=4, a=5))  # True

# 在定义函数时，我们可以在参数列表中用/设置强制位置参数（positional-only arguments），用*设置命名关键字参数。所谓强制位置参数，就是调用函数时只能按照参数位置来接收参数值的参数；而命名关键字参数只能通过“参数名=参数值”的方式来传递和接收参数，大家可以看看下面的例子。
# /前面的参数是强制位置参数
def make_judgement(a, b, c, /):
    """判断三条边的长度能否构成三角形"""
    return a + b > c and b + c > a and a + c > b
# *后面的参数是命名关键字参数
def make_judgement(*, a, b, c):
    """判断三条边的长度能否构成三角形"""
    return a + b > c and b + c > a and a + c > b

# 参数的默认值
from random import randrange


# 定义摇色子的函数
# 函数的自变量（参数）n表示色子的个数，默认值为2
# 函数的因变量（返回值）表示摇n颗色子得到的点数
def roll_dice(n=2):
    total = 0
    for _ in range(n):
        total += randrange(1, 7)
    return total
# 如果没有指定参数，那么n使用默认值2，表示摇两颗色子
print(roll_dice())
# 传入参数3，变量n被赋值为3，表示摇三颗色子获得点数
print(roll_dice(3))

def add(a=0, b=0, c=0):
    """三个数相加求和"""
    return a + b + c
# 调用add函数，没有传入参数，那么a、b、c都使用默认值0
print(add())         # 0
# 调用add函数，传入一个参数，该参数赋值给变量a, 变量b和c使用默认值0
print(add(1))        # 1
# 调用add函数，传入两个参数，分别赋值给变量a和b，变量c使用默认值0
print(add(1, 2))     # 3
# 调用add函数，传入三个参数，分别赋值给a、b、c三个变量
print(add(1, 2, 3))  # 6


# 可变参数
# 用星号表达式来表示args可以接收0个或任意多个参数
# 调用函数时传入的n个参数会组装成一个n元组赋给args
# 如果一个参数都没有传入，那么args会是一个空元组
def add(*args):
    total = 0
    # 对保存可变参数的元组进行循环遍历
    for val in args:
        # 对参数进行了类型检查（数值型的才能求和）
        if type(val) in (int, float):
            total += val
    return total
# 在调用add函数时可以传入0个或任意多个参数
print(add())         # 0
print(add(1))        # 1
print(add(1, 2, 3))  # 6
print(add(1, 2, 'hello', 3.45, 6))  # 12.45

# 如果我们希望通过“参数名=参数值”的形式传入若干个参数，具体有多少个参数也是不确定的，我们还可以给函数添加可变关键字参数，把传入的关键字参数组装到一个字典中，代码如下所示
# 参数列表中的**kwargs可以接收0个或任意多个关键字参数
# 调用函数时传入的关键字参数会组装成一个字典（参数名是字典中的键，参数值是字典中的值）
# 如果一个关键字参数都没有传入，那么kwargs会是一个空字典
def foo(*args, **kwargs):
    print(args)
    print(kwargs)
foo(3, 2.1, True, name='骆昊', age=43, gpa=4.95)
# (3, 2.1, True)
# {'name': '骆昊', 'age': 43, 'gpa': 4.95}


# 用模块管理函数
def foo():
    print('hello, world!')
foo()
# 但是如果项目是团队协作多人开发的时候，团队中可能有多个程序员都定义了名为foo的函数，这种情况下怎么解决命名冲突呢？答案其实很简单，Python 中每个文件就代表了一个模块（module），我们在不同的模块中可以有同名的函数，在使用函数的时候，我们通过import关键字导入指定的模块再使用完全限定名（模块名.函数名）的调用方式，就可以区分到底要使用的是哪个模块中的foo函数，代码如下所示。
# module1.py
def foo():
    print('hello, world!')
# module2.py
def foo():
    print('goodbye, world!')
# test.py
import module1
# 用“模块名.函数名”的方式（完全限定名）调用函数，
module1.foo()  # hello, world!

import module1 as m1
m1.foo()  # hello, world!

from module1 import foo
foo()  # hello, world!

from module1 import foo as f1
f1()  # hello, world!


# 标准库中的模块和函数
# abs	返回一个数的绝对值，例如：abs(-1.3)会返回1.3。
# bin	把一个整数转换成以'0b'开头的二进制字符串，例如：bin(123)会返回'0b1111011'。
# chr	将Unicode编码转换成对应的字符，例如：chr(8364)会返回'€'。
# hex	将一个整数转换成以'0x'开头的十六进制字符串，例如：hex(123)会返回'0x7b'。
# input	从输入中读取一行，返回读到的字符串。
# len	获取字符串、列表等的长度。
# max	返回多个参数或一个可迭代对象中的最大值，例如：max(12, 95, 37)会返回95。
# min	返回多个参数或一个可迭代对象中的最小值，例如：min(12, 95, 37)会返回12。
# oct	把一个整数转换成以'0o'开头的八进制字符串，例如：oct(123)会返回'0o173'。
# open	打开一个文件并返回文件对象。
# ord	将字符转换成对应的Unicode编码，例如：ord('€')会返回8364。
# pow	求幂运算，例如：pow(2, 3)会返回8；pow(2, 0.5)会返回1.4142135623730951。
# print	打印输出。
# range	构造一个范围序列，例如：range(100)会产生0到99的整数序列。
# round	按照指定的精度对数值进行四舍五入，例如：round(1.23456, 4)会返回1.2346。
# sum	对一个序列中的项从左到右进行求和运算，例如：sum(range(1, 101))会返回5050。
# type	返回对象的类型，例如：type(10)会返回int；而 type('hello')会返回st
