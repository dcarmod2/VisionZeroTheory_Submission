import datetime

def in_season(dt):
	dt_date=dt.date()
	if ((6,21)<=(dt_date.month,dt_date.day)<=(8,22)):
		return True
	else:
		return False



name="Manhattan Summer"
print(name)

def timewindower(dt):
    if (dt.isoweekday()>5):
    	return False #immediate return false if weekend
    return in_season(dt)
