import datetime

def in_season(dt):
	dt_date=dt.date()
	if ((8,22)<=(dt_date.month,dt_date.day)<=(12,21)):
		return True
	else:
		return False



name="Manhattan Fall"
print(name)

def timewindower(dt):
    if (dt.isoweekday()>5):
    	return False #immediate return false if weekend
    return in_season(dt)
