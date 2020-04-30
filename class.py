class A:
    def __getattr__(self, item):
        if item not in dir(self):
            return getattr(self, "get_name")
    
    def get_name(self):
        return "name"


a = A()
a.f1() # 当调用A类中没有的方法时, 会自动调用get_name方法
a.f2()

