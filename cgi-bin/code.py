#!/home/jamwal77/opt/python-3.6.2/bin/python3
#Created by Trey W.
import web
import os
import Day_Update as WA
from datetime import timedelta, date

urls = (
    '/', 'index',
    '/images/(.*)', 'images'
)

render = web.template.render('templates/')

class index:
    def GET(self):
        i = web.input(date = '')
        try:
            day = (web.websafe(i.date)).split(' ')
            rotation = WA.whatDay(day[0],day[1],day[2])
            longDate = date((int(day[2])), (int(WA.inv_months[day[0]])), (int(day[1])))
            if rotation == 'Key Error':
                if longDate.weekday() == 6:
                    longDate = longDate + timedelta(days=-2)
                elif longDate.weekday() == 5:
                    longDate = longDate + timedelta(days=2)
                day = WA.getLongDate(longDate)
                rotation = WA.whatDay(day[0],day[1],day[2])
        except:
            day = WA.date
            rotation = WA.whatDay(day[0],day[1],day[2])
            longDate = date((int(day[2])), (int(WA.inv_months[day[0]])), (int(day[1])))
        if rotation == 'Key Error' or rotation == 'Unknown Error':
            rotation = ''
        return render.index(rotation, WA.weekdays[str(longDate.weekday())], WA.getLunch(), WA.makeImage(rotation, 0.6), WA.getAun(), day)

class images:
    def GET(self,name):
        ext = name.split(".")[-1] # Gather extension

        cType = {
            "png":"images/png",
            "jpg":"images/jpeg",
            "gif":"images/gif",
            "ico":"images/x-icon"            }

        if name in os.listdir('images'):  # Security
            web.header("Content-Type", cType[ext]) # Set the Header
            return open('images/%s'%name,"rb").read() # Notice 'rb' for reading images
        else:
            raise web.notfound()

if __name__ == "__main__":
    web.config.debug = False
    app = web.application(urls, globals())
    app.run()
