import requests
import os
import math
from datetime import datetime, timedelta

import boto3


APP_ID = os.getenv("PCO_APP_ID")
SECRET = os.getenv("PCO_SECRET")

MEMBER_MANIFEST = list()

client = boto3.client('ses', 'us-west-2')


def main():

    formatted_date = datetime.now().strftime("%A, %B %d, %Y")

    get_member_list()

    number_of_members = math.ceil(len(MEMBER_MANIFEST)/days_in_month())
    today = datetime.now().day
    email = str.strip(build_email(
        MEMBER_MANIFEST[(datetime.now().day - 1):((today + number_of_members) - 1)],
        formatted_date
    ))

    aws_email(
        subject=f"Elder Daily Prayer - {formatted_date}",
        content=email,
        to_address=['crowemi@hotmail.com'],
    )


def get_member_list():
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

        if len(data) == 0:
            # no more members exist, break out
            process = False
            continue

        for j in data:
            member = {
                'id': member_iterator,
                'first_name': j["attributes"]["first_name"],
                'last_name': j["attributes"]["last_name"],
                'avatar': j["attributes"]["avatar"]
            }
            MEMBER_MANIFEST.append(member)
            member_iterator += 1

        offset += 25


def build_email(collection: list, formatted_date: str) -> str:
    email = "<html>"
    email += f'<h5>{formatted_date}</h5>'

    notes = ""

    for record in collection:
        name = f"{record['first_name']} {record['last_name']}"
        avatar = record['avatar']

        email += f'<table><tr><td style="vertical-align: text-top; padding:2px;"><img height="100" width="100" src="{avatar}"></td><td><table><tr><td style="vertical-align: text-top; padding:2px;"><h5>{name}</h5></td></tr><tr>{notes}</tr></table></td></tr></table>'

    email += "</html>"
    return email


def days_in_month():
    today = datetime.now()
    current_day = datetime(year=today.year, month=today.month, day=1)
    end_of_month = False
    days_in_month = 1

    while not end_of_month:
        next_day = current_day + timedelta(days=1)
        if next_day.month != current_day.month:
            end_of_month = True
            continue
        days_in_month += 1
        current_day = next_day

    return days_in_month


def aws_email(subject: str, to_address: list, content: str):
    resp = client.send_email(
        Source='no-reply@crowemi.com',
        Destination={
            'ToAddresses': to_address
        },
        Message={
            'Subject': {
                'Data': subject
            },
            'Body': {
                'Html': {
                    'Data': content
                }
            }
        }
    )


if __name__ == "__main__":
    main()
