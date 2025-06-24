from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Fund, SavedFund


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'token')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
            'token': {'read_only': True}
        }

    def validate(self, data):
        if User.objects.filter(username__iexact=data['username']).exists():
            raise serializers.ValidationError({'username': 'This username already exists'})
        if User.objects.filter(email__iexact=data.get('email', '')).exists():
            raise serializers.ValidationError({'email': 'This email is already registered'})
        return data

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                validated_data['username'],
                email=validated_data.get('email'),
                password=validated_data['password']
            )
            user.is_active = True
            user.save()
            from rest_framework.authtoken.models import Token
            token, _ = Token.objects.get_or_create(user=user)
            return user
        except Exception as e:
            raise serializers.ValidationError({'error': str(e)})

    def get_token(self, obj):
        from rest_framework.authtoken.models import Token
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = ('id', 'scheme_code', 'scheme_name')

    def create(self, validated_data):
        fund = Fund.objects.create(**validated_data)
        return fund

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data


class SavedFundSerializer(serializers.ModelSerializer):
    fund = FundSerializer(read_only=True)
    scheme_code = serializers.CharField(write_only=True)

    class Meta:
        model = SavedFund
        fields = ('id', 'fund', 'scheme_code')

    def create(self, validated_data):
        user = self.context['request'].user
        scheme_code = validated_data.pop('scheme_code')
        fund, _ = Fund.objects.get_or_create(scheme_code=scheme_code, defaults={'scheme_name': f'Fund {scheme_code}'})
        saved_fund = SavedFund.objects.create(user=user, fund=fund, **validated_data)
        return saved_fund

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email')
