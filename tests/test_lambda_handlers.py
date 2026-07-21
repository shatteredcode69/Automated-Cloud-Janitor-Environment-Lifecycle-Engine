from datetime import datetime, timezone

import compliance_checker
import janitor


class DummySNSClient:
    def __init__(self):
        self.published = []

    def publish(self, TopicArn, Subject, Message):
        self.published.append({"TopicArn": TopicArn, "Subject": Subject, "Message": Message})
        return {"MessageId": "123"}


def test_compliance_checker_alerts_when_required_tags_missing(monkeypatch):
    sns_client = DummySNSClient()
    monkeypatch.setenv("SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:cloud-janitor")
    monkeypatch.setattr(compliance_checker, "get_sns_client", lambda: sns_client)

    event = {
        "detail": {
            "responseElements": {
                "instancesSet": {
                    "items": [
                        {
                            "instanceId": "i-123",
                            "tags": [{"key": "Owner", "value": "platform"}],
                        }
                    ]
                }
            }
        }
    }

    result = compliance_checker.lambda_handler(event, None)

    assert result["statusCode"] == 200
    assert len(sns_client.published) == 1
    assert "missing required tags" in sns_client.published[0]["Message"].lower()


def test_select_expired_instances_terminates_expired_ttl():
    now = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)
    instances = [
        {
            "InstanceId": "i-expired",
            "LaunchTime": datetime(2026, 7, 20, 8, 0, tzinfo=timezone.utc),
            "Tags": [{"Key": "TTL", "Value": "24"}],
        },
        {
            "InstanceId": "i-active",
            "LaunchTime": datetime(2026, 7, 20, 20, 0, tzinfo=timezone.utc),
            "Tags": [{"Key": "TTL", "Value": "72"}],
        },
    ]

    expired_ids = janitor.select_expired_instance_ids(instances, now)

    assert expired_ids == ["i-expired"]
