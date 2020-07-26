#!/usr/bin/env python3

import boto3
import json
import pytz
import uuid
from datetime import datetime
from faker import Faker

fake = Faker()
kinesis = boto3.client('kinesis')


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            # AWS Redshift TIMESTAMP format YYYY-MM-DD HH24:MI:SS
            return obj.strftime("%Y-%m-%d %H:%M:%S")


class CreditCard:
    def __init__(self, card_type: str, card_owner: str, card_number: str, card_cvc: str, card_state: str):
        self.card_type = card_type
        self.card_owner = card_owner
        self.card_number = card_number
        self.card_cvc = card_cvc
        self.card_state = card_state

    def __str__(self):
        return (f"card_type: {self.card_type}\n"
                f"card_owner: {self.card_owner}\n"
                f"card_number: {self.card_number}\n"
                f"card_cvc: {self.card_cvc}\n"
                f"card_state: {self.card_state}\n")


class Transaction:
    def __init__(self, tx_id: str, tx_amount_cents: int, tx_currency: str, cc: CreditCard):
        self.tx_id = tx_id
        self.tx_amount_cents = tx_amount_cents
        self.tx_currency = tx_currency
        self.credit_card = cc

    def __str__(self):
        return (f"tx_id: {self.tx_id}\n"
                f"payment_amount_cents: {self.payment_amount_cents}\n"
                f"payment_curreny: {self.payment_curreny}\n"
                f"credit_card: {self.credit_card}\n")


class PaymentEvent:
    def __init__(self, tx: Transaction):
        self.event_created = datetime.now(pytz.timezone("UTC"))
        self.event_type = "PAYMENT_EVENT"
        self.event_json_data = json.dumps(tx, default=lambda o: o.__dict__)


def generate_tx(cc: CreditCard) -> Transaction:
    tx_amount_cents = fake.pyint(min_value=1000, max_value=100000, step=1000)
    return Transaction(uuid.uuid4().hex, tx_amount_cents, "EUR", cc)
    return tx


def push_event(tx: Transaction):
    payment_event = PaymentEvent(tx)
    data = DateTimeEncoder().encode(payment_event.__dict__)
    print(data)
    kinesis.put_record(StreamName="PaymentStream",
                       Data=data,
                       PartitionKey="single_shard")

def handler(event, context):
    for _ in range(100):
        str_cc = fake.credit_card_full().splitlines()
        cc = CreditCard(card_type=str_cc[0].split()[0],
                        card_owner=str_cc[1],
                        card_number=str_cc[2].split()[0],
                        card_cvc=str_cc[2].split()[1],
                        card_state="LEGIT" if fake.pyint(min_value=0, max_value=99, step=1) > 9 else "STOLEN")

        if cc.card_state == "STOLEN":
            for _ in range(5):
                push_event(generate_tx(cc))
        else:
            push_event(generate_tx(cc))

    return {
        "requestId": event['requestId'],
        "status": "SUCCESS"
    }

# handler({"requestId": "requestId"}, None)