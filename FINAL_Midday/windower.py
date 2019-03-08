import datetime

name="Manhattan midday"
print(name)

(start_midday,end_midday)=(10,15) # 9 AM to 4 PM
window_length = 6
def timewindower(dt):
    if (dt.isoweekday()>5):
    	return False #immediate return false if weekend
    return start_midday<= dt.hour <= end_midday
