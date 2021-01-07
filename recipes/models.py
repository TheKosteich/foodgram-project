from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name='Ingredient name'
    )
    dimension = models.CharField(
        max_length=16,
        verbose_name='Ingredient dimension unit'
    )

    def __str__(self):
        return f'{self.title} - {self.dimension}'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='recipe_images')
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredients')
    is_breakfast = models.BooleanField(default=False)
    is_lunch = models.BooleanField(default=False)
    is_dinner = models.BooleanField(default=False)
    cooking_time = models.IntegerField()
    slug = models.SlugField()

    def __str__(self):
        return f'{self.title} - {self.author.username}'


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='choosers'
    )

    def __str__(self):
        return f'{self.user.username} - {self.recipe.title}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followings'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )

    class Meta:
        unique_together = ['user', 'following']

    def __str__(self):
        return f'{self.user.username} following {self.following.username}'


class UserPurchases(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='purchases')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='purchases')
    amount = models.IntegerField()
