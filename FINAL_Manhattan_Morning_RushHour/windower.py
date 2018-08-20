import datetime

name="Manhattan morning rush hour"
print(name)

(start_morning_rush,end_morning_rush)=(7,9) # 7 to 9 AM
window_length = 3
def timewindower(dt):
    if (dt.isoweekday()>5):
    	return False #immediate return false if weekend
    return (start_morning_rush<=dt.hour<=end_morning_rush)
