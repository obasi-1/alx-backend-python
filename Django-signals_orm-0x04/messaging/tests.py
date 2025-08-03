# messaging/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessagingSignalsTest(TestCase):
    """
    Test suite for the Django signals in the messaging app.
    """
    def setUp(self):
        """
        Set up two test users for the messaging tests.
        """
        self.sender = User.objects.create_user(username='sender', password='password123')
        self.receiver = User.objects.create_user(username='receiver', password='password123')

    def test_notification_creation_on_new_message(self):
        """
        Test that a new Notification is created when a new Message is saved.
        """
        # Initially, there should be no notifications
        self.assertEqual(Notification.objects.count(), 0)

        # Create a new message
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello there!"
        )

        # Check that a notification has been created
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()

        # Check that the notification's user and message are correct
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message.sender, self.sender)
        self.assertEqual(notification.message.content, "Hello there!")
        self.assertFalse(notification.is_read)
