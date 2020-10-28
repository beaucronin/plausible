import os
import boto3

def handler(event, context):
    config = load_config()
    nw_event = NarrowWaistEvent.create(event)
    for output in config.outputs:
        pass


class NarrowWaistEvent(object):
    def __init__(self, event_type, raw_event):
        super().__init__()
        self.raw_event = raw_event
    
    @classmethod
    def create(cls, event):
        event_type = cls.identify_event(event)
        if not event_type:
            return None
        nwe = NarrowWaistEvent(event_type, event)
        return nwe

    @classmethod
    def identify_event(event):
        if 'Records' in event:
            record = event["Records"][0]
            es = record.get("eventSource", record.get("EventSource", ""))
            if es == "aws:dynamodb":
                return "dynamodb"
            elif es == "aws:kinesis":
                return "kinesis"
            elif es == "aws:sns":
                return "sns"
            elif es == "aws:sqs":
                return "sqs"
        elif "awslogs" in event:
            return "logs"
        elif "detail" in event and "detail-type" in event:
            return "eventbridge"
        elif "payload" in event and "detector" in event["payload"]:
            return "iotevents"
        else:
            return None
    
    