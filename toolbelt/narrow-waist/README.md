# Narrow Waist Lambda

## Lambda event sources

| Source Service | Source Type | Invocation Type | Payload Format | Permissions |
| --- | --- | --- | --- | --- |
| [API Gateway](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html) | [Integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html) | [Synchronous](https://docs.aws.amazon.com/lambda/latest/dg/invocation-sync.html) | | |
| [CloudWatch Events](https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchevents.html) | Event | [Asynchronous](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html) | CloudWatch Event JSON | |
| [CloudWatch Logs](https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchlogs.html) | [Subscription](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Subscriptions.html) | [Asynchronous](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html) | zipped, Base64 | |
| [DynamoDB](https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html) | [EventSourceMapping](https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html) | [Synchronous](https://docs.aws.amazon.com/lambda/latest/dg/invocation-sync.html) | `Records` `aws.dynamodb` | |
| [IoT](https://docs.aws.amazon.com/lambda/latest/dg/services-iot.html) | [Rule](https://docs.aws.amazon.com/iot/latest/developerguide/iot-rules.html) | [Asynchronous](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html) | Arbitrary JSON | |
| [IoT Events](https://docs.aws.amazon.com/lambda/latest/dg/services-iotevents.html) | | [Asynchronous](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html) | IoT Event JSON| |
| [Kinesis](https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html) | [EventSourceMapping](https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html) | [Synchronous](https://docs.aws.amazon.com/lambda/latest/dg/invocation-sync.html) | `Records` `aws.kinesis` | |
| [SNS](https://docs.aws.amazon.com/lambda/latest/dg/with-sns.html) | [Subscription](https://docs.aws.amazon.com/sns/latest/dg/sns-lambda-as-subscriber.html) | [Asynchronous](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async.html) | `Records` `aws.sns` | |
| [SQS](https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html) | [EventSourceMapping](https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html) | [Synchronous](https://docs.aws.amazon.com/lambda/latest/dg/invocation-sync.html) | `Records` `aws.sqs` | |
