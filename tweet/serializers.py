from rest_framework import serializers
from django.contrib.auth.models import User
from tweet.models import Tweet, RequestAction, AdminActions, Logs

class TweetSerializer(serializers.HyperlinkedModelSerializer):
    created_by_name = serializers.SerializerMethodField()
    updated_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = "__all__"

    def get_created_by_name(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"

    def get_updated_by_name(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"


class CreateUpdateDeleteTweetSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Tweet.objects.all(), required=False)
    text = serializers.CharField(max_length=280, min_length=1)
    image_url = serializers.URLField(required=False)
    created_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    updated_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=False)

    def create(self, attrs):
        current_user = self.context['request'].user
        tweet = Tweet(text=attrs.get('text'), 
                    image_url=attrs.get('image_url'), 
                    created_by=current_user, updated_by=current_user)
        tweet.save()
        return TweetSerializer(tweet, context=self.context).data

    def update(self, obj, attrs):
        if not attrs.get('text') and not attrs.get('image_url'):
            raise serializers.ValidationError("At least one of image_url or text is required")
        obj.text = attrs.get('text') or obj.text
        obj.image_url = attrs.get('image_url') or obj.image_url
        obj.updated_by = self.context['request'].user
        obj.save()
        return obj


class RequestActionSerializer(serializers.HyperlinkedModelSerializer):
    created_for = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    updated_by_name = serializers.SerializerMethodField()

    class Meta:
        model = RequestAction
        fields = "__all__"

    def get_created_for(self, obj):
        return f"{obj.created_for.first_name} {obj.created_for.last_name}"

    def get_created_by_name(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"

    def get_updated_by_name(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"


class CreateDeleteRequestActionSerializer(serializers.ModelSerializer):
    created_for = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    tweet = serializers.PrimaryKeyRelatedField(queryset=Tweet.objects.all(), required=False)
    action = serializers.ChoiceField(choices=[(tag.value, tag) for tag in AdminActions], required=False)
    created_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    updated_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=False)

    class Meta:
        model  = RequestAction
        exclude = ('is_approved',)

    def validate(self, attrs):
        if not attrs.get('created_for') and attrs.get('action') == AdminActions.create.value:
            # created_for is mandatory for "CREATE"
            raise serializers.ValidationError("created_for is mandatory for admins")    
        if attrs.get('action') in {AdminActions.create.value, AdminActions.update.value}:
            if not attrs.get('tweet_content', ''):
                # tweet_content is mandatory for "CREATE/UPDATE"
                raise serializers.ValidationError("Create/Update action must have tweet content")
        return attrs

    def create(self, attrs):
        current_user = self.context['request'].user
        created_for = attrs.get('created_for')
        if not created_for or attrs['action'] == AdminActions.update.value:
            created_for = attrs['tweet'].created_by
        action = RequestAction(
                    tweet_content=attrs['tweet_content'],
                    created_for=created_for,
                    created_by=current_user,
                    action=attrs['action'],
                    updated_by=current_user,
                    tweet=attrs.get('tweet')
                )
        action.save()
        return action

class UpdateRequestActionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = RequestAction
        fields = ['is_approved']

    def update(self, obj, attrs):
        if obj.is_approved:
            raise serializers.ValidationError("Action is already approved")
        current_user = self.context['request'].user
        if attrs['is_approved'] and current_user.is_superuser:
            obj.updated_by = current_user
            obj.approve()
        return obj

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = "__all__"
