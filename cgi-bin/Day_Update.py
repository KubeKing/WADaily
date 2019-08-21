#!/home/jamwal77/opt/python-3.6.2/bin/python3
#Created by Trey W.
import requests
import json
from lxml import html
from ics import Calendar
from datetime import datetime, date, timedelta
from PIL import Image

weekdays = {'0':'Monday','1':'Tuesday','2':'Wednesday','3':'Thursday','4':'Friday','5':'Saturday','6':'Sunday'}
months = {'1':'January','2':'February','3':'March','4':'April','5':'May',
'6':'June','7':'July','8':'August','9':'September','10':'October','11':'November','12':'December'}
inv_months = {v: k for k, v in months.items()}
months_abv = {'January':'Jan', 'February':'Feb'}
storedSchedule = eval(open('ScheduleDictStorage.txt', 'r').read())

def getLongDate(x):
    date = x.timetuple()
    year = str(date.tm_year)
    month = str(date.tm_mon)
    day = str(date.tm_mday)
    return([(months[month]),(day),(str(year))])

def getShortDate(m,d,y):
    return(datetime((int(y)), (int(inv_months[str(m)])), (int(d))))

def getLunch(d, m, y):
    lm = str(inv_months[str(m)])
    if int(lm) <= 9:
        lm = '0'+str(lm)
    try:
        with open('json_cache/lunchList.json') as json_file:
            data = json.load(json_file)
        return(data[str(y)+'-'+str(lm)+'-'+str(d)])
    except:
        try:
            page = requests.get('https://woodward.nutrislice.com/menu/api/weeks/school/upper-school/menu-type/lunch/'+str(y)+'/'+lm+'/'+str(d)+'/?format=json')
            tree = html.fromstring(page.content)
            allText = tree.xpath('//*/text()')[0]
            allText = json.loads(allText)
            menu = {}
            for day in allText['days']:
                li = []
                for holder in day['menu_items']:
                    if holder['food'] and holder['food']['name']:
                        li.append(holder['food']['name'])
                menu[day['date']] = li[:8]
            try:
                with open('json_cache/lunchList.json', 'w') as outfile:
                    json.dump(menu, outfile)
                return(menu[str(y)+'-'+str(lm)+'-'+str(d)])
            except:
                return('')
        except:
            return('')

def getAun(d, m, y):
    try:
        with open('json_cache/aunList.json') as json_file:
            data = json.load(json_file)
    except:
        data, data['Updated'] = {}, None
    try:
        if data['Updated'] == str(date.today()):
            return(data[str(m)+'/'+str(d)+'/'+str(y)])
        else:
            c = Calendar(requests.get('https://www.woodward.edu/calendar/calendar_368.ics').text)
            c, aunDict, lastDate = c.events, {}, []
            c.reverse()
            for item in c:
                if item.name:
                    dateMod = getLongDate(item.begin)
                    if lastDate == dateMod:
                        aunDict[str(dateMod[0])+'/'+str(dateMod[1])+'/'+str(dateMod[2])].append(item.name)
                    else:
                        aunDict[str(dateMod[0])+'/'+str(dateMod[1])+'/'+str(dateMod[2])] = [item.name]
                    lastDate = dateMod
            try:
                aunDict['Updated'] = str(date.today())
                with open('json_cache/aunList.json', 'w') as outfile:
                    json.dump(aunDict, outfile)
                return(aunDict[str(m)+'/'+str(d)+'/'+str(y)])
            except:
                return('')
    except:
        return('')

def whatDay(m,d,y,doMath):
    try:
        longDate = [m,d,y]
        day = storedSchedule[m+' '+d+' '+y]
    except KeyError:
        if doMath == True:
            shortDate = getShortDate(m,d,y)
            if shortDate.weekday() == 6:
                longDate = getLongDate(shortDate + timedelta(days=-2))
                try:
                    day = storedSchedule[longDate[0]+' '+longDate[1]+' '+longDate[2]]
                except:
                    day = 'Key Error'
            elif shortDate.weekday() == 5 or shortDate.weekday() == '5':
                longDate = getLongDate(shortDate + timedelta(days=2))
                try:
                    day = storedSchedule[longDate[0]+' '+longDate[1]+' '+longDate[2]]
                except:
                    day = 'Key Error'
            else:
                day = 'Key Error'
        else:
            day = 'Key Error'
    except:
        day = 'Unknown Error'
    return(day, longDate)

def makeImage(rotation, scale):
    if rotation != 'Unknown Error' and rotation != '' and rotation != 'Key Error':
        size = (Image.open('images/'+rotation.replace(' ', '')+'.jpg')).size
        image = {'src':('../images/'+rotation.replace(' ', '')+'.jpg'),'alt':rotation,'width':str(size[0]* scale),'height':str(size[1]* scale),
            'bottomPadding':str((size[1]* scale)/2)+'px','halfWidth':str((size[0]* scale)/2)}
        rotation = ('a '+rotation)
    else:
        image = {'src':'', 'bottomPadding':'-10px', 'halfWidth':'0', 'height':'0'}
    return(image)

def week_range(idate):
    fastDate = str(date.today())
    year, week, dow = idate.isocalendar()
    try:
        with open('json_cache/weekData.json') as json_file: 
            data = json.load(json_file)
    except:
        data = {}
    try:
        holder = data[str(week)+'/'+str(year)]
        if holder['Updated'] == fastDate:
            return(holder)
    except:
        pass
    weekData = {'rotations': [], 'misc': {}}
    if dow == 7:
        start_date = idate
    else:
        start_date = idate - timedelta(dow)

    n = start_date + timedelta(1)
    for i in range(5):
        try:
            loDa = getLongDate(n)
            x = {'rotation':(makeImage((whatDay(loDa[0], loDa[1], loDa[2], False))[0], 0.65)), 'day':weekdays[str(n.weekday())][:3]}
            if x['rotation']['src']:
                weekData['rotations'].append(x)
        except:
            pass
        n = n + timedelta(1)
    tallest = 0
    days = weekData['rotations']
    for i in days:
        try:
            if float(i['rotation']['height']) > tallest:
                tallest = float(i['rotation']['height'])
        except:
            pass
    for i in days:
        i['rotation']['bottomPadding'] = ((str((tallest - float(i['rotation']['height']))/2))+'px')
    weekData['misc']['tallest'] = ((str(tallest/2))+'px')
    weekData['Updated'] = fastDate
    data[str(week)+'/'+str(year)] = weekData
    with open('json_cache/weekData.json', 'w') as outfile:
        json.dump(data, outfile)
    return(weekData)

if __name__ == "__main__":
    pass #For testing