from rest_framework import serializers

from .models import Account, Business, Category


class CostomerAccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "id",
            "username",
            "name",
            "last_Name",
            "email",
            "phone",
            "birthday",
            "gender",
            "education",
            "social_media",
        )


class LeaderboardCostomerAccountSerializers(serializers.ModelSerializer):
    profile_image = serializers.ImageField(
        max_length=None, use_url=False, allow_null=True, required=False
    )

    class Meta:
        model = Account
        fields = ("id", "username", "name", "last_Name", "profile_image")


class AccountSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ("id", "username", "name", "last_Name", "email", "phone", "password")

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class AccountReedSerializers(serializers.ModelSerializer):
    profile_image = serializers.ImageField(
        max_length=None, use_url=False, allow_null=True, required=False
    )

    class Meta:
        model = Account
        fields = (
            "id",
            "name",
            "last_Name",
            "username",
            "phone",
            "country",
            "city",
            "email",
            "is_Business",
            "address",
            "profile_image",
        )


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BusinessSerializers(serializers.ModelSerializer):
    account = AccountReedSerializers()
    profile_image = serializers.ImageField(
        max_length=None, use_url=False, allow_null=True, required=False
    )

    # category = CategorySerializers()
    class Meta:
        model = Business
        fields = "__all__"


class BusinessBaeseSerializers(serializers.ModelSerializer):
    profile_image = serializers.ImageField(
        max_length=None, use_url=False, allow_null=True, required=False
    )

    class Meta:
        model = Business
        fields = "__all__"


class BusinessWriteeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = (
            "account",
            "category",
            "Nationalcode",
            "web_address",
            "social_network",
            "shop_address",
            "B_phone",
            "online",
            "ofline",
        )


class BusinessImageWriteeSerializers(serializers.ModelSerializer):
    profile_image = serializers.ImageField(
        max_length=None, use_url=False, allow_null=True, required=False
    )

    class Meta:
        model = Business
        fields = ["profile_image"]


class AccountImageWriteeSerializers(serializers.ModelSerializer):
    profile_image = serializers.ImageField(
        max_length=None, use_url=False, allow_null=True, required=False
    )

    class Meta:
        model = Account
        fields = ["profile_image"]
