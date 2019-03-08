import datetime

name="Manhattan weekdays"
print(name)

def timewindower(dt):
    if (dt.isoweekday()>5):
    	return False #immediate return false if weekend
    return True
