import datetime

name="Manhattan weekend"
print(name)

def timewindower(dt):
    if (dt.isoweekday()>5):
    	return True #immediate return true if weekend
    return False
