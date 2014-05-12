
# The derivative of the sunset times gives you the number 
# of minutes more per day available.

# nice example code i stole:
# http://datadebrief.blogspot.com/2010/10/plotting-sunrise-sunset-times-in-python.html

import ephem
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm
import datetime




plt.figure()
cx = matplotlib.cm.coolwarm_r

mo = ['Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan']

place = ephem.city('Seattle')


start_date = datetime.datetime(2014,1,1,12) # yyyy,m,d,h - midday is best
end_date = datetime.datetime(2015, 1, 1,12) 

sun = ephem.Sun(place)

dates = []
sunrise = []
sunset = []

numdays = (end_date - start_date).days
dates = [start_date + datetime.timedelta(days=i) for i in xrange(numdays+1)] 
dates.sort()


def dt2m(dt):
    return dt.hour + dt.minute/60. + dt.second/3600.

sunrise = map(lambda x:dt2m(ephem.localtime(place.next_rising(sun,start=x))),dates)
sunset = map(lambda x:dt2m(ephem.localtime(place.next_setting(sun,start=x))),dates)

place.lon='-140'
place.elev = 100.

pLat = map(lambda x:str(x), range(0,60,5))
for k in range(0,len(pLat)):
    place.lat = pLat[k]


    daylen = map(lambda x:( (place.next_setting(sun,start=x) - 
                            place.next_rising(sun,start=x)) % 1 )*24.*60.,dates)
    
    d_daylen = np.diff(daylen,n=1)
    plt.plot_date(dates[1:],d_daylen,'-',color=cx(k / float(len(pLat))))


tmp = plt.xticks()
plt.xticks(tmp[0], mo)
plt.ylabel('Length of Day Change (min)')
xpos = (tmp[0][8]+tmp[0][7])/2.
plt.text(xpos, 0.2, 'Equator',color=cx(0))
xpos = (tmp[0][1]+tmp[0][1])/2.
plt.text(xpos, 5., '55$^\circ$ lat',color=cx(k / float(len(pLat))))
plt.ylim(-6,6)
plt.savefig('delta_time.png',dpi=250)
plt.close()



plt.figure()
plt.plot_date(dates,sunrise,'r-')
plt.plot_date(dates,sunset,'b-')
plt.xticks(tmp[0], mo)
plt.ylabel('Sun Rise/Set Time')
plt.ylim(0,24)
plt.title('SEATTLE')
plt.savefig('riseset_time.png',dpi=250)
plt.close()

