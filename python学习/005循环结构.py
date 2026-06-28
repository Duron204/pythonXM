import time

print('hello, world')
time.sleep(1) #停顿一秒然后结束

# for-in循环
# 每隔1秒输出一次“hello, world”，持续1小时
import time

for i in range(3600):
    print('hello, world')
    time.sleep(1)

# 每隔1秒输出一次“hello, world”，持续1小时
import time

for _ in range(3600):
    print('hello, world')
    time.sleep(1)

# 从1到100的整数求和
total = 0
for i in range(1, 101):
    total += i
print(total)

# 从1到100的偶数求和
total = 0
for i in range(1, 101):
    if i % 2 == 0:
        total += i
print(total)

# 从1到100的偶数求和
total = 0
for i in range(2, 101, 2):
    total += i
print(total)

# 从1到100的偶数求和
print(sum(range(2, 101, 2)))

# while循环
# 从1到100的整数求和
total = 0
i = 1
while i <= 100:
    total += i
    i += 1
print(total)

# 从1到100的偶数求和
total = 0
i = 2
while i <= 100:
    total += i
    i += 2
print(total)

# break和continue
# 从1到100的偶数求和
total = 0
i = 2
while True:
    total += i
    i += 2
    if i > 100:
        break
print(total) 

# 从1到100的偶数求和
total = 0
for i in range(1, 101):
    if i % 2 != 0:
        continue
    total += i
print(total)

# 嵌套的循环结构
# 打印乘法口诀表
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f'{i}×{j}={i * j}', end='\t')
    print()

# 循环结构的应用
# 例子1：判断素数
# 要求：输入一个大于 1 的正整数，判断它是不是素数。
# 输入一个大于1的正整数判断它是不是素数
num = int(input('请输入一个正整数: '))
end = int(num ** 0.5)
is_prime = True
for i in range(2, end + 1):
    if num % i == 0:
        is_prime = False
        break
if is_prime:
    print(f'{num}是素数')
else:
    print(f'{num}不是素数')

# 例子2：最大公约数
# 输入两个正整数求它们的最大公约数
x = int(input('x = '))
y = int(input('y = '))
for i in range(x, 0, -1):
    if x % i == 0 and y % i == 0:
        print(f'最大公约数: {i}')
        break

# 输入两个正整数求它们的最大公约数
x = int(input('x = '))
y = int(input('y = '))
while y % x != 0:
    x, y = y % x, x
print(f'最大公约数: {x}')

# 例子3：猜数字游戏
# 猜数字小游戏
import random
answer = random.randrange(1, 101)
counter = 0
while True:
    counter += 1
    num = int(input('请输入: '))
    if num < answer:
        print('大一点.')
    elif num > answer:
        print('小一点.')
    else:
        print('猜对了.')
        break
print(f'你一共猜了{counter}次.')