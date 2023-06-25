from pulumi_aws import sns


class SnsTopics(object):
    def __init__(self):
        self.error_notification_topic = sns.Topic(
            "ErrorNotificationTopic",
            args=sns.TopicArgs(display_name="error-notifications"),
        )
        sns.TopicSubscription(
            "ErrorNotificationToEmail",
            topic=self.error_notification_topic,
            protocol="email-json",
            confirmation_timeout_in_minutes=10,
            endpoint="illia.sorokoumov@gmail.com",
        )
