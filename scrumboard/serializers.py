from rest_framework import serializers
from scrumboard.models import List, Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


class ListSerializer(serializers.ModelSerializer):
    # line below lists scrum cards in list directly
    cards = CardSerializer(read_only=True, many=True)

    class Meta:
        model = List
        fields = '__all__'
