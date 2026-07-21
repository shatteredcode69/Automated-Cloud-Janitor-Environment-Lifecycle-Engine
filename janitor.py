from datetime import datetime, timezone


def select_expired_instance_ids(instances, now=None):
    if now is None:
        now = datetime.now(timezone.utc)

    expired_ids = []
    for instance in instances:
        tags = instance.get("Tags", []) or []
        ttl_value = None
        for tag in tags:
            if tag.get("Key") == "TTL":
                ttl_value = tag.get("Value")
                break
        if ttl_value is None:
            continue

        try:
            ttl_hours = int(ttl_value)
        except (TypeError, ValueError):
            continue

        launch_time = instance.get("LaunchTime")
        if not isinstance(launch_time, datetime):
            continue

        age_hours = (now - launch_time).total_seconds() / 3600
        if age_hours >= ttl_hours:
            expired_ids.append(instance.get("InstanceId"))

    return expired_ids


def lambda_handler(event, context):
    now = datetime.now(timezone.utc)
    instances = event.get("instances", [])
    expired_ids = select_expired_instance_ids(instances, now)
    return {"statusCode": 200, "expiredInstanceIds": expired_ids}
