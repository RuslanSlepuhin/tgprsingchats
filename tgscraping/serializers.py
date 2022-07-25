from rest_framework import serializers

from models import TelegramChatsView


class ParsingTelegramSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramChatsView
        fields = '__all__'


class GetTelegramSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramChatsView
        fields = '__all__'