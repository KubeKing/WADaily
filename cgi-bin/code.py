#!/home/jamwal77/opt/python-3.6.2/bin/python3
#Created by Trey W.
import web
import os
import Day_Update as WA
from datetime import date, datetime

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
            rotation = WA.whatDay(day[0],day[1],day[2],True)
        except:
            day = [(WA.months[str(datetime.now().month)]), (str(datetime.now().day)), (str(datetime.now().year))]
            rotation = WA.whatDay(day[0],day[1],day[2],False)
        return render.index(rotation[0], WA.weekdays[str(WA.getShortDate(rotation[1][0], rotation[1][1], rotation[1][2]).weekday())], WA.getLunch(rotation[1][1], rotation[1][0], rotation[1][2]), WA.makeImage(rotation[0], 0.6), WA.getAun(rotation[1][1]), rotation[1])

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
    web.config.debug = True
    app = web.application(urls, globals())
    app.run()
