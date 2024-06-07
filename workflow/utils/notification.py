class NotificationService:
    """
    Service for sending notifications.

    Methods:
        send(message: str): Sends a notification with the given message.
    """

    def send(self, message: str):
        """
        Sends a notification with the given message.

        Args:
            message (str): The message to be sent as a notification.
        """
        print(message)


def get_notification_service() -> NotificationService:
    """
    Returns an instance of the NotificationService class.

    Returns:
        NotificationService: An instance of the NotificationService class.
    """
    return NotificationService()
