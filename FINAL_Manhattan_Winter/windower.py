import datetime

def in_season(dt):
	dt_date=dt.date()
	if ((12,21)<=(dt_date.month,dt_date.day)<=(12,31) or (1,1) <= (dt_date.month,dt_date.day)<= (3,20)):
		return True
	
	else:
		return False



name="Manhattan Winter"
print(name)

def timewindower(dt):
    if (dt.isoweekday()>5):
    	return False #immediate return false if weekend
    return in_season(dt)
