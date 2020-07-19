#!/usr/bin/env python3

import boto3
import json
import pytz
from datetime import datetime
from faker import Faker


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            # AWS Redshift TIMESTAMP format YYYY-MM-DD HH24:MI:SS
            return obj.strftime("%Y-%m-%d %H:%M:%S")


class CreditCard:
    def __init__(self, card_type: str, card_owner: str, card_number: str, card_cvc: str, card_state: str,
                 payment_amount: int):
        self.card_type = card_type
        self.card_owner = card_owner
        self.card_number = card_number
        self.card_cvc = card_cvc
        self.card_state = card_state
        self.payment_amount = payment_amount

    def __str__(self):
        return (f"card_type: {self.card_type}\n"
                f"card_owner: {self.card_owner}\n"
                f"card_number: {self.card_number}\n"
                f"card_cvc: {self.card_cvc}\n"
                f"card_state: {self.card_state}\n"
                f"payment_amount: {self.payment_amount}\n")


class PaymentEvent:
    def __init__(self, cc: CreditCard):
        self.event_created = datetime.now(pytz.timezone("UTC"))
        self.event_type = "PAYMENT_EVENT"
        self.event_json_data = json.dumps(cc.__dict__)


def handler(event, context):
    kinesis = boto3.client('kinesis')
    fake = Faker()

    for _ in range(100):
        str_cc = fake.credit_card_full().splitlines()
        cc = CreditCard(card_type=str_cc[0].split()[0],
                        card_owner=str_cc[1],
                        card_number=str_cc[2].split()[0],
                        card_cvc=str_cc[2].split()[1],
                        card_state="LEGIT" if fake.pyint(min_value=0, max_value=99, step=1) > 9 else "STOLEN",
                        payment_amount=fake.pyint(min_value=1000, max_value=100000, step=1000)
                        )

        payment_event = PaymentEvent(cc)
        data = DateTimeEncoder().encode(payment_event.__dict__)
        print(data)

        if cc.card_state == "STOLEN":
            for _ in range(5):
                kinesis.put_record(StreamName="PaymentStream",
                                   Data=data,
                                   PartitionKey="single_shard")
        else:
            kinesis.put_record(StreamName="PaymentStream",
                               Data=data,
                               PartitionKey="single_shard")

    return {
        "requestId": event['requestId'],
        "status": "SUCCESS"
    }
