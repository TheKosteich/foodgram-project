from django.contrib.auth import get_user_model
from django.db import models
from taggit.managers import TaggableManager

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name='Имя ингредиента'
    )
    dimension = models.CharField(
        max_length=16,
        verbose_name='Единицы измерения ингредиента'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.title} - {self.dimension}'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes', verbose_name='Автор')
    title = models.CharField(max_length=256, verbose_name='Имя рецепта')
    image = models.ImageField(upload_to='recipe_images',
                              verbose_name='Изображение рецепта')
    description = models.TextField(verbose_name='Текст рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты рецепта'
    )
    tags = TaggableManager(verbose_name='Теги рецепта')
    cooking_time = models.IntegerField(verbose_name='Время приготовления')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.title} - {self.author.username}'

    def get_absolute_url(self):
        return f'/recipes/{self.id}/'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_ingredients',
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   verbose_name='Ингредиент')
    amount = models.IntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='choosers',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='Уникальный избранный рецепт')
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.title}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followings',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='Уникальная подписка')
        ]

    def __str__(self):
        return f'{self.user.username} following {self.following.username}'


class RecipeToShopping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='recipes_to_shopping',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='shopping_users',
                               verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Рецепт для покупки'
        verbose_name_plural = 'Рецепты для покупки'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='Уникальный рецепт для покупки')
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'
