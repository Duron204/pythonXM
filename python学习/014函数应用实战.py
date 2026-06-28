# 例子1：随机验证码
# 设计一个生成随机验证码的函数，验证码由数字和英文大小写字母构成，长度可以通过参数设置。
import random
import string
ALL_CHARS = string.digits + string.ascii_letters
def generate_code(*, code_len=4):
    """
    生成指定长度的验证码
    :param code_len: 验证码的长度(默认4个字符)
    :return: 由大小写英文字母和数字构成的随机验证码字符串
    """
    return ''.join(random.choices(ALL_CHARS, k=code_len))
# 说明1：string模块的digits代表0到9的数字构成的字符串'0123456789'，string模块的ascii_letters代表大小写英文字母构成的字符串'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'。
# 说明2：random模块的sample和choices函数都可以实现随机抽样，sample实现无放回抽样，这意味着抽样取出的元素是不重复的；choices实现有放回抽样，这意味着可能会重复选中某些元素。这两个函数的第一个参数代表抽样的总体，而参数k代表样本容量，需要说明的是choices函数的参数k是一个命名关键字参数，在传参时必须指定参数名。
for _ in range(5):
    print(generate_code()) 
for _ in range(5):
    print(generate_code(code_len=6))


# 例子2：判断素数
# 设计一个判断给定的大于1的正整数是不是质数的函数。质数是只能被1和自身整除的正整数（大于1），如果一个大于1的正整数N是质数，那就意味着在2到N−1之间都没有它的因子。
def is_prime(num: int) -> bool:
    """
    判断一个正整数是不是质数
    :param num: 大于1的正整数
    :return: 如果num是质数返回True，否则返回False
    """
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


# 例子3：最大公约数和最小公倍数
def lcm(x: int, y: int) -> int:
    """求最小公倍数"""
    return x * y // gcd(x, y)

def gcd(x: int, y: int) -> int:
    """求最大公约数"""
    while y % x != 0:
        x, y = y % x, x
    return x


# 例子4：数据统计
def ptp(data):
    """极差（全距）"""
    return max(data) - min(data)
def mean(data):
    """算术平均"""
    return sum(data) / len(data)
def median(data):
    """中位数"""
    temp, size = sorted(data), len(data)
    if size % 2 != 0:
        return temp[size // 2]
    else:
        return mean(temp[size // 2 - 1:size // 2 + 1])
def var(data, ddof=1):
    """方差"""
    x_bar = mean(data)
    temp = [(num - x_bar) ** 2 for num in data]
    return sum(temp) / (len(temp) - ddof)
def std(data, ddof=1):
    """标准差"""
    return var(data, ddof) ** 0.5
def cv(data, ddof=1):
    """变异系数"""
    return std(data, ddof) / mean(data)
def describe(data):
    """输出描述性统计信息"""
    print(f'均值: {mean(data)}')
    print(f'中位数: {median(data)}')
    print(f'极差: {ptp(data)}')
    print(f'方差: {var(data)}')
    print(f'标准差: {std(data)}')
    print(f'变异系数: {cv(data)}')

# 例子5：双色球随机选号
# 双色球随机选号程序
import random

RED_BALLS = [i for i in range(1, 34)]
BLUE_BALLS = [i for i in range(1, 17)]
def choose():
    """
    生成一组随机号码
    :return: 保存随机号码的列表
    """
    selected_balls = random.sample(RED_BALLS, 6)
    selected_balls.sort()
    selected_balls.append(random.choice(BLUE_BALLS))
    return selected_balls
def display(balls):
    """
    格式输出一组号码
    :param balls: 保存随机号码的列表
    """
    for ball in balls[:-1]:
        print(f'\033[031m{ball:0>2d}\033[0m', end=' ')
    print(f'\033[034m{balls[-1]:0>2d}\033[0m')
n = int(input('生成几注号码: '))
for _ in range(n):
    display(choose())
# 大家看看display(choose())这行代码，这里我们先通过choose函数获得一组随机号码，然后把choose函数的返回值作为display函数的参数，通过display函数将选中的随机号码显示出来。重构之后的代码逻辑非常清晰，代码的可读性更强了。如果有人为你封装了这两个函数，你仅仅是函数的调用者，其实你根本不用关心choose函数和display函数的内部实现，你只需要知道调用choose函数可以生成一组随机号码，而调用display函数传入一个列表，就可以输出这组号码。将来我们使用各种各样的 Python 三方库时，我们也根本不关注它们的底层实现，我们需要知道的仅仅是调用哪个函数可以解决问题。

