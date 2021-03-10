#!/usr/bin/python3
import requests
import time
from datetime import datetime, timedelta

def getApiRepo(URL, HEADERS, language, timediff):
    since = datetime(2014, 8, 31)
    until = since + timedelta(days=timediff)
    repositories = []
    counter1 = 0

    while until < (datetime.today() + timedelta(days=timediff)):
        day_url = URL.replace('SINCE', since.strftime('%Y-%m-%d')).replace('UNTIL', until.strftime('%Y-%m-%d')).replace('LANGUAGE', language)
        r = requests.get(day_url, headers=HEADERS)
        print(f'Repositories created between {since.strftime("%Y-%m-%d")} and {until.strftime("%Y-%m-%d")}: {r.json().get("total_count")}')
        counter1 += int(r.json().get("total_count"))
        # Traverse pagination
        while 'next' in r.links.keys():
            r = requests.get(r.links['next']['url'], headers=HEADERS)
            #Extract Data
            for rep in r.json()["items"]:
                repositories.append(rep["html_url"])
            time.sleep(7) #To respect api rate limit
        #Extract Data
        for rep in r.json()["items"]:
            repositories.append(rep["html_url"])
        time.sleep(7)
        # Update dates for the next search
        since = until
        until = since + timedelta(days=timediff)
    print("Reel nb repo = " + str(counter1))
    return repositories

if __name__ == "__main__":
    URL = f'https://api.github.com/search/repositories?q=language:LANGUAGE%20created:SINCE..UNTIL&per_page=100'
    HEADERS = {'Authorization': 'e10788310b8e6abe53a33bd6bec37545f0170a66'}
    timediff = 20

    repositories = getApiRepo(URL, HEADERS, "Solidity", timediff)
    print("Total repo : " + str(len(repositories)))
    print(len(set(repositories)))
