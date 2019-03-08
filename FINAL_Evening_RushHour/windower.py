import datetime

name="Manhattan evening rush hour"
print(name)

(start_evening_rush,end_evening_rush)=(16,18) # 4 to 6 PM
window_length = 3
def timewindower(dt):
    if (dt.isoweekday()>5):
    	return False #immediate return false if weekend
    return (start_evening_rush<=dt.hour<=end_evening_rush)
