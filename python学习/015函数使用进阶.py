# 高阶函数
def calc(*args, **kwargs):
    items = list(args) + list(kwargs.values())
    result = 0
    for item in items:
        if type(item) in (int, float):
            result += item
    return result
# 如果我们希望上面的calc函数不仅仅可以做多个参数的求和，还可以实现更多的甚至是自定义的二元运算，我们该怎么做呢？上面的代码只能求和是因为函数中使用了+=运算符，这使得函数跟加法运算形成了耦合关系，如果能解除这种耦合关系，函数的通用性和灵活性就会更好。解除耦合的办法就是将+运算符变成函数调用，并将其设计为函数的参数，代码如下所示。
def calc(init_value, op_func, *args, **kwargs):
    items = list(args) + list(kwargs.values())
    result = init_value
    for item in items:
        if type(item) in (int, float):
            result = op_func(result, item)
    return result
# 注意，上面的函数增加了两个参数，其中init_value代表运算的初始值，op_func代表二元运算函数，为了调用修改后的函数，我们先定义做加法和乘法运算的函数，代码如下所示。
def add(x, y):
    return x + y
def mul(x, y):
    return x * y
# 如果要做求和的运算，我们可以按照下面的方式调用calc函数。
print(calc(0, add, 1, 2, 3, 4, 5))  # 15
# 如果要做求乘积运算，我们可以按照下面的方式调用calc函数。
print(calc(1, mul, 1, 2, 3, 4, 5))  # 120 
