import datetime

name="Manhattan whole day"
print(name)

(day_start,day_end) = (0,23)
window_length = 24
def timewindower(dt):
    if (dt.isoweekday()>5):
    	return False #immediate return false if weekend
    return (day_start<=dt.hour<=day_end)
