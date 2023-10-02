from rest_framework import serializers

from django.contrib.auth.models import User

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'user_name')

    def validate_user_name(self, user_name):
        print(User.objects.all())
        if not User.objects.filter(username=user_name).exists():
            raise serializers.ValidationError('User with this username does not exists.')
        return user_name