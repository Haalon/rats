from django.contrib.auth.models import Group
from rats.api.models import User, Ingredient, Recipe, Quantity, Tag
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['url', 'name', 'calories', 'proteins', 'fats', 'carbs']


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        fields = ['url', 'name','description', 'instructions', 'author', 'ingredients', 'difficulty', 'time_to_cook', 'tags']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'name']

class QuantitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Quantity
        fields = ['url', 'recipe', 'ingredient', 'measure', 'ratio', 'amount']