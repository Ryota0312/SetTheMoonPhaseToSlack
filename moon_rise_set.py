import datetime
import requests
import json
import yaml
import xmltodict
import os

SLACK_STATUS_API = 'https://slack.com/api/users.profile.set'
MOON_API = 'http://labs.bitmeister.jp/ohakon/api/'

try:
    SLACK_TOKEN = yaml.load(open('settings.yml','r'))['slack_token']
except:
    SLACK_TOKEN = os.environ["SLACK_TOKEN"]

def get_moon_status(lat, lng, y, m, d):
    result = requests.get(url=MOON_API, params={'mode': 'moon_rise_set', 'year': y, 'month': m, 'day': d, 'lat': lat, 'lng': lng})
    return xmltodict.parse(result.text)


def update_status(emoji, text):
    data = {
        'token': SLACK_TOKEN,
        'profile': json.dumps({'status_text': text, 'status_emoji': emoji})
    }
    result = requests.post(url=SLACK_STATUS_API, data=data)
    return result

def moonage2emoji(ma):
    if ma >= 0 and ma < 1: return ":new_moon:"
    if ma >= 1 and ma < 6: return ":waxing_crescent_moon:"
    if ma >= 6 and ma < 10: return ":first_quarter_moon:"
    if ma >= 10 and ma < 13.8: return ":waxing_gibbous_moon:"
    if ma >= 13.8 and ma <= 15.8: return ":full_moon:"
    if ma > 15.8 and ma < 20: return ":waning_gibbous_moon:"
    if ma >= 20 and ma < 24: return ":last_quarter_moon:"
    if ma >= 24 and ma < 29: return ":waning_crescent_moon:"
    if ma >= 29 and ma < 30: return ":new_moon:"
    return ":full_moon_with_face:"

def main():
    date = datetime.date.today()
    
    moon_info = get_moon_status(yaml.load(open('settings.yml','r'))['lat'], yaml.load(open('settings.yml','r'))['lng'], date.year, date.month, date.day)
    if moon_info["result"]["rise_and_set"]["moonrise_hm"]=="--:--":
        datey = date - datetime.timedelta(days=1)
        moon_info_yesterday = get_moon_status(yaml.load(open('settings.yml','r'))['lat'], yaml.load(open('settings.yml','r'))['lng'], datey.year, datey.month, datey.day)
        moonrise = "前" + moon_info_yesterday["result"]["rise_and_set"]["moonrise_hm"]
    else:
        moonrise = moon_info["result"]["rise_and_set"]["moonrise_hm"]
    if moon_info["result"]["rise_and_set"]["moonset_hm"]=="--:--":
        datet = date + datetime.timedelta(days=1)
        moon_info_tommorow = get_moon_status(yaml.load(open('settings.yml','r'))['lat'], yaml.load(open('settings.yml','r'))['lng'], datet.year, datet.month, datet.day)
        moonset = "翌" + moon_info_tommorow["result"]["rise_and_set"]["moonset_hm"]
    else:
        moonset = moon_info["result"]["rise_and_set"]["moonset_hm"]
        
    status_text = "月齢: " + moon_info["result"]["moon_age"] + " 月出: " + moonrise + " 月没: "  + moonset + " (" + yaml.load(open('settings.yml','r'))['city'] + "," + str(date.year) + "/" + str(date.month) + "/" + str(date.day) + ")"
    
    emoji = moonage2emoji(float(moon_info["result"]["moon_age"]))
    #print(emoji)
    #print(status_text)

    res = update_status(emoji, status_text)
    #print(res.json())

if __name__ == '__main__':
    main()
