class testclass1:
        def testfunc1(self):
            print(f"test accomplished with number {self.number}")
            


class testclass2(testclass1):
    def __init__(self, number):
        self.number = number

testobj = testclass2(42)
testobj.testfunc1()