from django.db import models


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
