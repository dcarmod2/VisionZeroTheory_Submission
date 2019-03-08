import datetime

name="Manhattan evening and morning"
print(name)

(day_start,day_end)=(7,18) # 7AM to 6 PM
window_length = 7 + 5
def timewindower(dt):
    if (dt.isoweekday()>5):
    	return False #immediate return false if weekend
    return not (day_start<=dt.hour<=day_end)
