from stonklib import getMinGain
import datetime

today = datetime.date.today()
friday = today + datetime.timedelta( (4-today.weekday()) % 7 )

print(friday,"Max Pain:",getMinGain("GME",friday))