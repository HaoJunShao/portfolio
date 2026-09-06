#定义类————不推荐，会降低可读性，可维护性
#无法看出对象的属性！
# class Car:
#     pass
# c1 = Car()
#动态的为对象添加属性
# c1.color = "red"
# c1.brand = "BMW"
# c1.name = "X5"
# c1.price = 500000
# print(c1)
# print(c1.__dict__)
# print(c1.brand)

#定义类
class Car:
    #__init__:初始化方法，会在对象创建时自动调用，可以在该方法中为对象设置对应属性
    #self：是第一个参数，表示当前所创建出来的实例对象
    def __init__(self,c_brand,c_name,c_price):
        self.brand = c_brand
        self.name = c_name
        self.price = c_price
        print("Car类型的对象初始化完毕，对象属性添加完毕")


# c2 = Car()
# print(c2.__dict__)

#实例方法
    def running(self):
        print(f"{self.brand}{self.name}正在高速行驶中")
    def total_price(self,discount,rate):
        """
        提车总费用
        :param discount:
        :param rate:
        :return:
        """
        return self.price*discount+rate*self.price
c1 = Car("BYD",'汉',200000)
c1.running()
print(c1.total_price(2,0.1))

