import json
import requests
import os 
import math
from datetime import datetime, timedelta

# from pco.people.person import Person

APP_ID = os.getenv("PCO_APP_ID") 
SECRET = os.getenv("PCO_SECRET") 

MEMBER_MANIFEST = list()

def main():

    member_iterator = 1
    offset = 0
    process = True 

    while process: 
        # authenticate
        resp = requests.get(
            f'https://api.planningcenteronline.com/people/v2/people?order=last_name&where[membership]=Member&where[status]=active&offset={offset}',
            auth=(APP_ID, SECRET)
        )

        data = resp.json()["data"]
        print(f"Active member count: {len(data)}")

        if len(data) == 0: 
            # no more members exist, break out
            process = False
            continue

        for j in data:
            member = {
                'id' : member_iterator,
                'first_name': j["attributes"]["first_name"],
                'last_name': j["attributes"]["last_name"],
                'avatar': j["attributes"]["avatar"]
            }
            print(member)
            MEMBER_MANIFEST.append(member)
            member_iterator += 1


        offset += 25

    print(len(MEMBER_MANIFEST))
    print(math.ceil(len(MEMBER_MANIFEST)/days_in_month()))


def days_in_month(): 
    today = datetime.now()
    current_day = datetime(year=today.year, month=today.month, day=1)
    end_of_month = False 
    days_in_month = 1
    
    while end_of_month == False:
        next_day = current_day + timedelta(days=1)
        if next_day.month != current_day.month:
            end_of_month = True
            continue 
        days_in_month += 1
        current_day = next_day

    return days_in_month

if __name__ == "__main__":
    main()
