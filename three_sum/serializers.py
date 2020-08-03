from rest_framework import serializers
from .models import Transactions


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ['input_list', 'target', 'result', 'queried_at']


class ThreeSumSerializer(serializers.Serializer):
    input_list = serializers.ListField()
    sum = serializers.IntegerField()

    def validate(self, attrs):
        if not attrs['input_list'] or len(str(attrs['input_list'])) <= 2:
            raise serializers.ValidationError("Invalid Input List")
        if not attrs['sum']:
            raise serializers.ValidationError("Invalid target value")
        return attrs




