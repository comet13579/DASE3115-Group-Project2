class TestCounter:
    def __init__(self, covid_disabled=False):
        self.counter = 0

    def getyear(self):
        if self.counter <= 2:
            return 2010
        else:
            return (self.counter - 3) // 12 + 2011

    def getmonth(self):
        if self.counter <= 2:
            return self.counter + 10
        else:
            return (self.counter - 3) % 12 + 1

    def getcounter(self):
        return self.counter

    def progress(self):
        if self.counter <= 119:
            self.counter += 1
        else:
            raise StopIteration

    def month_minus_1(year:int,month:int):
        if month != 1:
            return (year,month - 1)
        else:
            return (year - 1,12)

if __name__ == '__main__':
    test = TestCounter()
    for _ in range(120):
        year = test.getyear()
        month = test.getmonth()
        print(f"Counter: {test.counter}, Year: {year}, Month: {month}")
        test.progress()
