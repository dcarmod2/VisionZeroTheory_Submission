import datetime

name="Manhattan party hours"
print(name)
window_length = 4 + 1
def timewindower(dt):
    if (dt.isoweekday()>5):
    	return False #immediate return false if weekend
    return dt.hour < 4 or dt.hour > 22
