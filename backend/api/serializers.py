from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj):
        return True  # пока так
