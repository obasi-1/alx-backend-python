from rest_framework import serializers
from .models import User, Conversation, Message

# User Serializer
# This serializer handles the User model.
# It exposes the user_id, username, email, first_name, last_name, and phone_number.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Fields to be included in the serialized output.
        # 'user_id' is the primary key.
        # 'username', 'email', 'first_name', 'last_name' are inherited from AbstractUser.
        # 'phone_number' is a custom field.
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']
        # 'read_only_fields' ensures these fields cannot be updated via the serializer.
        # 'user_id' is typically read-only as it's a primary key generated automatically.
        read_only_fields = ['user_id']

    # Example of using serializers.CharField for custom validation or non-model fields
    # If you had a field not directly mapped to a model, or needed specific validation
    # custom_field = serializers.CharField(max_length=100, required=False)

    # Example of using serializers.ValidationError in a custom validation method
    # def validate_email(self, value):
    #     if User.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("This email is already in use.")
    #     return value


# Message Serializer
# This serializer handles the Message model.
# It exposes message_id, conversation, sender, message_body, and sent_at.
class MessageSerializer(serializers.ModelSerializer):
    # 'sender' is a ForeignKey to User. We want to display the sender's username, not just their ID.
    # Using a StringRelatedField will display the __str__ method of the User model.
    sender = serializers.StringRelatedField(read_only=True)
    # Alternatively, if you want more details about the sender, you could nest the UserSerializer:
    # sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        # Fields to be included in the serialized output.
        # 'message_id' is the primary key.
        # 'conversation' is the ForeignKey to Conversation.
        # 'sender' is the ForeignKey to User.
        # 'message_body' is the content of the message.
        # 'sent_at' is the timestamp.
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']
        # 'read_only_fields' ensures these fields cannot be updated via the serializer.
        read_only_fields = ['message_id', 'sent_at']


# Conversation Serializer
# This serializer handles the Conversation model, with nested relationships.
# It exposes conversation_id, participants, name, created_at, updated_at, and messages.
class ConversationSerializer(serializers.ModelSerializer):
    # 'participants' is a ManyToManyField to User.
    # We use UserSerializer(many=True) to serialize multiple User objects for participants.
    # read_only=True means participants cannot be added/removed directly via this serializer on creation/update.
    # If you need to manage participants via the serializer, you'd need to override create/update methods.
    participants = UserSerializer(many=True, read_only=True)

    # 'messages' is a Reverse ForeignKey relationship from Message to Conversation.
    # We use MessageSerializer(many=True) to serialize multiple Message objects.
    # read_only=True means messages cannot be created/updated directly via this nested serializer.
    # source='messages' refers to the related_name defined in the Message model's ForeignKey to Conversation.
    messages = MessageSerializer(many=True, read_only=True, source='messages')

    # Example of using serializers.SerializerMethodField()
    # This field will return a custom value computed by a method on the serializer.
    # Here, it returns a comma-separated string of participant usernames.
    participant_usernames = serializers.SerializerMethodField()
    # Another example: message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        # Fields to be included in the serialized output.
        # 'conversation_id' is the primary key.
        # 'participants' will be a list of serialized User objects.
        # 'name' is the conversation name.
        # 'created_at' and 'updated_at' are timestamps.
        # 'messages' will be a list of serialized Message objects.
        # 'participant_usernames' is our new custom field.
        fields = ['conversation_id', 'participants', 'name', 'created_at', 'updated_at', 'messages', 'participant_usernames']
        # 'read_only_fields' ensures these fields cannot be updated via the serializer.
        read_only_fields = ['conversation_id', 'created_at', 'updated_at']

    # Method for participant_usernames SerializerMethodField
    def get_participant_usernames(self, obj):
        # 'obj' refers to the current Conversation instance being serialized
        return ", ".join([p.username for p in obj.participants.all()])

    # Example method for message_count SerializerMethodField
    # def get_message_count(self, obj):
    #     return obj.messages.count()

    # Example of using serializers.ValidationError in a custom validation method for the whole serializer
    # def validate(self, data):
    #     # Example: Ensure a conversation has at least two participants if 'name' is not provided
    #     if not data.get('name') and len(data.get('participants', [])) < 2:
    #         raise serializers.ValidationError("A conversation without a name must have at least two participants.")
    #     return data
