import datetime

name="Manhattan night"
print(name)

(start_evening_rush,end_evening_rush)=(18,23) # 6 to 11 PM
window_length = 6
def timewindower(dt):
    if (dt.isoweekday()>5):
    	return False #immediate return false if weekend
    return (start_evening_rush<=dt.hour<=end_evening_rush)
