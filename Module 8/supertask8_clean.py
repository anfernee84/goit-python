from datetime import datetime
import calendar
from collections import defaultdict


people = [
    {"vasya": datetime(year=2002, month=7, day=27)},
    {"pasha": datetime(year=1997, month=8, day=1)},
    {"masha": datetime(year=1980, month=7, day=29)},
    {"vika": datetime(year=1991, month=8, day=10)},
    {"pedro": datetime(year=1975, month=7, day=30)},
    {"gena": datetime(year=1983, month=8, day=12)},
    {"anne": datetime(year=2000, month=7, day=28)},
    {"kate": datetime(year=1998, month=8, day=14)},
    {"chubrik": datetime(year=1995, month=7, day=25)},
    {"arkadiy": datetime(year=1993, month=8, day=12)}
    
]

week = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

def congratulate(guys: list):
    btday_now = defaultdict(list)
    btday_then = defaultdict(list)
    strtofyear = datetime(year=datetime.now().year, month=1, day=1)
    for person in people:
        for n, d in person.items():
            d = d.replace(year=datetime.now().year)
            weeknow = (datetime.now() - strtofyear).days //7
            btdayweek = (d - strtofyear).days // 7
        if weeknow == btdayweek:
            if d.weekday() > 4:
                btday_then[0].append(d)
            else:
                btday_now[d.weekday()].append(n)
        if btdayweek == weeknow + 1:
            btday_then[d.weekday()].append(n)    
    btday_then.pop(0)
    
    
    print("Now we will congratulate next guys: \n")  
    for i in sorted(btday_now.items()):
        borned = "; ".join(i[1])
        print(f"{week[i[0]]}: {borned}")
    
    print("\nNext week we will congratulate next guys: \n")
    for i in sorted(btday_then.items()):
        borned = "; ".join(i[1])
        print(f"{week[i[0]]}: {borned}")



congratulate(people)