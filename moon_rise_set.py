import datetime
import requests
import json
import yaml
import xmltodict

SLACK_STATUS_API = 'https://slack.com/api/users.profile.set'
MOON_API = 'http://labs.bitmeister.jp/ohakon/api/'

SLACK_TOKEN = yaml.load(open('settings.yml','r'))['slack_token']


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
    moon_info = get_moon_status(34.54, 133.92, date.year, date.month, date.day)
    status_text = "月齢: " + moon_info["result"]["moon_age"] + " 月出: " + moon_info["result"]["rise_and_set"]["moonrise_hm"] + " 月没: "  + moon_info["result"]["rise_and_set"]["moonset_hm"] + " (岡山市," + str(date.year) + "/" + str(date.month) + "/" + str(date.day) + ")"
    emoji = moonage2emoji(float(moon_info["result"]["moon_age"]))
    #print(emoji)
    #print(status_text)

    res = update_status(emoji, status_text)
    #print(res.json())

if __name__ == '__main__':
    main()
