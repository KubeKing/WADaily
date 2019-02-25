from ics import Calendar
import requests

weekdays = {'0':'Monday','1':'Tuesday','2':'Wednesday','3':'Thursday','4':'Friday','5':'Saturday','6':'Sunday'}
months = {'1':'January','2':'February','3':'March','4':'April','5':'May',
'6':'June','7':'July','8':'August','9':'September','10':'October','11':'November','12':'December'}
inv_months = {v: k for k, v in months.items()}

def getLongDate(x):
    date = x.timetuple()
    year = str(date.tm_year)
    month = str(date.tm_mon)
    day = str(date.tm_mday)
    return([(months[month]),(day),(str(year))])

c = Calendar(requests.get('https://woodward.finalsite.com/calendar/calendar_400.ics').text)
c, foodDict = c.events, {}
c.reverse()

for item in c:
    if item.description:
        dateMod = getLongDate(item.begin)
        food = (item.description).split('\n')
        food = [value for value in food if value != '']
        foodDict[str(dateMod[0])+'/'+str(dateMod[1])+'/'+str(dateMod[2])] = food


def getLunch(d, m, y):
    try:
        with open('lunchList.json') as json_file: 
            data = json.load(json_file) 
            return(str(m)+'/'+str(d)+'/'+str(y)])
    except:
        try:
            c = Calendar(requests.get('https://woodward.finalsite.com/calendar/calendar_400.ics').text)
            c, foodDic = c.events, {}
            c.reverse()
            for item in c:
                if item.description:
                    dateMod = getLongDate(item.begin)
                    food = (item.description).split('\n')
                    food = [value for value in food if value != '']
                    foodDict[str(dateMod[0])+'/'+str(dateMod[1])+'/'+str(dateMod[2])] = food
            try:
                with open('lunchList.json', 'w') as outfile:
                    json.dump(foodDict, outfile)
                return(foodDict[str(m)+'/'+str(d)+'/'+str(y)])
            except:
                return('')
        except:
            return('')