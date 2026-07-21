import os


def get_sns_client():
    import boto3

    return boto3.client("sns")


def extract_instance_items(event):
    detail = event.get("detail", {})
    response_elements = detail.get("responseElements", {})
    instances_set = response_elements.get("instancesSet", {})
    items = instances_set.get("items", [])
    return items


def validate_instance_tags(instance):
    required_tags = {"Owner", "Environment", "TTL"}
    tags = instance.get("tags", [])
    tag_map = {tag.get("key", "").strip(): tag.get("value", "") for tag in tags if isinstance(tag, dict)}
    missing = sorted(required_tags - set(tag_map.keys()))
    return missing


def lambda_handler(event, context):
    topic_arn = os.getenv("SNS_TOPIC_ARN")
    if not topic_arn:
        return {"statusCode": 200, "body": "SNS_TOPIC_ARN not configured"}

    instances = extract_instance_items(event)
    sns_client = get_sns_client()
    published = []

    for instance in instances:
        instance_id = instance.get("instanceId", "unknown")
        missing_tags = validate_instance_tags(instance)
        if missing_tags:
            message = (
                f"Instance {instance_id} is missing required tags: {', '.join(missing_tags)}"
            )
            sns_client.publish(
                TopicArn=topic_arn,
                Subject="Cloud Janitor Compliance Alert",
                Message=message,
            )
            published.append(message)

    return {"statusCode": 200, "body": f"Processed {len(instances)} instances", "published": published}
