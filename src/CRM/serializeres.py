from rest_framework import serializers
from .models import consulting,Category

# ---- کلاس ساخته شده برای drf
class consultingSerializers(serializers.ModelSerializer):
    class Meta:
        model = consulting 
        fields = '__all__'
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = '__all__'