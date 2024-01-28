from django.db import models


class Product(models.Model):
    """
    Модель продукта
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название продукта'
    )
    usage_count = models.IntegerField(
        default=0,
        verbose_name='Количество использований'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['pk']


class Recipe(models.Model):
    """
    Модель рецепта
    """
    name = models.CharField(
        max_length=255,
        verbose_name='Название рецепта'
    )
    products = models.ManyToManyField(
        Product,
        through='RecipeProduct',
        related_name='recipes',
        verbose_name='Продукты для рецепта'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['pk']


class RecipeProduct(models.Model):
    """
    Модель продуктов в рецепте
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_query_name="recipe_product",
        verbose_name='Рецепт'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_query_name="recipe_product",
        verbose_name='Продукт'
    )
    weight = models.IntegerField(
        verbose_name='Вес'
    )

    def __str__(self):
        return f"{self.recipe.name} - {self.product.name} ({self.weight}g)"

    class Meta:
        verbose_name = 'Продукт в рецепте'
        verbose_name_plural = 'Продукты в рецептах'
        ordering = ['pk']
