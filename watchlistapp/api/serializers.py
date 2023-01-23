from dataclasses import fields
from platform import platform
from wsgiref.validate import validator
from rest_framework import serializers

from watchlistapp.models import Review, watchlist,StreamPlatform



# class StreamPlatformSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = StreamPlatform
#         fields = "__all__"
class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        exclude = ('watchlist',)
        # fields = "__all__"

class watchlistSerializer(serializers.ModelSerializer):
    # Review=ReviewSerializer(read_only=True, many=True,source='reviews')
    platform = serializers.CharField(source='platform.name')
    # len_name = serializers.SerializerMethodField()

    class Meta:
        model = watchlist
        fields =  "__all__"


    def create(self, validated_data):
        return validated_data


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = watchlistSerializer(many=True,read_only=True)

    class Meta:
        model = StreamPlatform
        fields = "__all__"






    # def get_len_name(self,object):
    #     print(object)
    #     length=len(object.tittle)
    #     return length
        
    # def validate(self,data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("name and description should be different!")
    #     else:
    #         return data


    # def validate(self,value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("name is too short!")
    #     else:
    #         return value



# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("name is too short!")



# class MovieSearializer(serializers.Serializer):
#     id =serializers.IntegerField(read_only=True)
#     name =serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active =serializers.BooleanField()




#     def create(self, validated_data):
#         return movie.objects.create(**validated_data)

#     def update(self,instance,validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance


#     def validate(self,data):
#         # import pdb;pdb.set_trace()
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("name and description should be different!")
#         else:
#             return data



#     # def validate_name(self,value):
#     #     if len(value)<2:
#     #         raise serializers.ValidationError('name too short!')
#     #     else:
#     #         return value
