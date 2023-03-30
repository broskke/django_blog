from rest_framework import serializers
from .models import Article, Tag, Comment, Rating, Like
from django.db.models import Avg

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        representation['tag'] = [tag.title for tag in instance.tag.all()]
        representation['rating'] = instance.ratings.aggregate(Avg('rate'))['rate__avg']
        # aggregate() -> {'rate__avg': 3.8}
        return representation
    

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id','title','tag', 'user')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'title']
        

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'user', 'article', 'text', 'created_at', 'updated_at', 'sub_comment')
        read_only_fields = ['article',]
# {
#     "title":"Post N2",
#     "description":"Some reandom description",
#     "tag":[
#         1,2
#     ]

# }

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'user', 'article', 'rate')
        read_only_fields = ['user', 'article']
        # unique_together = ['user', 'article']
        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset = model.objects.all(),
        #         fields=('user','article'),
        #         message='Вы уже ставили рейтинг !'
        #     )
        # ]

    def validate(self, attrs):
        user = self.context.get('request').user
        article = self.context.get('article')
        rate = Rating.objects.filter(user=user, article=article).exists()
        if rate:
            raise serializers.ValidationError({'message': 'Rate already exists'})
        



    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)
    
