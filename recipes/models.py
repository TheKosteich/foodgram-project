from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy
from taggit.managers import TaggableManager

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
    tags = TaggableManager()
    cooking_time = models.IntegerField()
    slug = models.SlugField()

    def __str__(self):
        return f'{self.title} - {self.author.username}'

    def get_absolute_url(self):
        return f'recipes/{self.id}/'


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_ingredients')
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

    class Meta:
        unique_together = ['user', 'recipe']

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

    class Meta:
        unique_together = ['user', 'ingredient']

    def __str__(self):
        return f'{self.user} - {self.ingredient}'


class RecipesToShopping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='recipes_to_shopping')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='users')
    count = models.IntegerField()

    class Meta:
        unique_together = ['user', 'recipe']

    def __str__(self):
        return f'{self.user} - {self.recipe}'
