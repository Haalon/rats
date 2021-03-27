from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from datetime import timedelta

# dirty hack for now
def defaultUser():
    try:
        res = User.objects.get(username='admin')
    except User.DoesNotExist:
        res = User.objects.create(username='admin', password='adminadmin', email='admin@admin')

    return res

# this will make the email required
class User(AbstractUser):
    email = models.EmailField(blank=False)


class Ingredient(models.Model):
    name = models.CharField(max_length=128)

    calories = models.FloatField(default=0, verbose_name='Calories per 100g')
    proteins = models.FloatField(default=0, verbose_name='Proteins per 100g')
    fats = models.FloatField(default=0, verbose_name='Fats per 100g')
    carbs = models.FloatField(default=0, verbose_name='Carbohydrates per 100g')

    def __str__(self):
        return self.name


class LowkeyField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(LowkeyField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()

class Tag(models.Model):
    name = LowkeyField(max_length=32)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=128)

    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)

    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        default=defaultUser,
        related_name='recipes'
    )

    time_to_cook = models.DurationField(default=timedelta(minutes=10))

    class Difficulty(models.TextChoices):
        EASY = 'E', 'Easy'
        MEDIUM = 'M', 'Medium'
        HARD = 'H', 'Hard'

    difficulty = models.CharField(
        max_length=1,
        choices=Difficulty.choices,
        default=Difficulty.EASY,
    )
    tags = models.ManyToManyField(Tag, blank=True)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Quantity'
    )

    def __str__(self):
        return self.name


class Quantity(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    # cups, liters, items, whatever
    measure = models.CharField(max_length=32, default='g')
    # ratio will be needed to convert fat\energy\etc values of an ingredient
    ratio = models.FloatField(default=100, verbose_name='Measures per 100g')
    amount = models.FloatField()
