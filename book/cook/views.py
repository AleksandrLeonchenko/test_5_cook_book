from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Q, F
from django.shortcuts import render
from django.http import HttpResponse
from .models import Recipe, Product, RecipeProduct

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Subquery, OuterRef


def add_product_to_recipe(request):
    """
    Обработчик GET-запроса для добавления продукта к рецепту.
    http://127.0.0.1:8000/add_product_to_recipe/?recipe_id=1&product_id=2&weight=200

    Parameters:
        request (HttpRequest): GET-запрос.

    Returns:
        JsonResponse: JSON-ответ с результатом операции.
    """
    if request.method == 'GET':
        try:
            recipe_id = int(request.GET['recipe_id'])
            product_id = int(request.GET['product_id'])
            weight = int(request.GET['weight'])
        except KeyError as e:
            return JsonResponse({'error': f'Отсутствует обязательный параметр: {e}'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Неверный формат параметров'}, status=400)
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        product = get_object_or_404(Product, pk=product_id)
        try:
            recipe_product = RecipeProduct.objects.get(recipe=recipe, product=product)
            recipe_product.weight = weight
            recipe_product.save()
            return JsonResponse(
                {'message': f'Продукт {product.name} добавлен к рецепту {recipe.name} с весом {weight} г.'})
        except ObjectDoesNotExist:
            RecipeProduct.objects.create(recipe=recipe, product=product, weight=weight)
            return JsonResponse(
                {'message': f'Продукт {product.name} добавлен к рецепту {recipe.name} с весом {weight} г.'})
        except Exception as e:
            return JsonResponse({'error': f'Ошибка при обработке запроса: {str(e)}'}, status=500)


def cook_recipe(request):
    """
    Обработчик GET-запроса для приготовления рецепта.
    http://127.0.0.1:8000/cook_recipe/?recipe_id=1

    Parameters:
        request (HttpRequest): GET-запрос.

    Returns:
        JsonResponse: JSON-ответ с результатом операции.
    """
    if request.method == 'GET':
        try:
            recipe_id = int(request.GET['recipe_id'])
        except KeyError as e:
            return JsonResponse({'error': f'Отсутствует обязательный параметр: {e}'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Неверный формат параметров'}, status=400)

        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe_products = recipe.recipeproduct_set.all()
        try:
            Product.objects.filter(recipe_product__in=recipe_products).update(usage_count=F('usage_count') + 1)
            return JsonResponse({'message': f'Количество приготовленных блюд для рецепта {recipe.name} увеличено'})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Рецепт не найден'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Ошибка при обработке запроса: {str(e)}'}, status=500)


def show_recipes_without_product(request):
    """
    Обработчик GET-запроса для отображения рецептов без указанного продукта.
    http://127.0.0.1:8000/show_recipes_without_product/?product_id=1

    Parameters:
        request (HttpRequest): GET-запрос.

    Returns:
        render: HTML-страница с результатом операции.
    """
    product_id = request.GET.get('product_id')

    if not product_id:
        return JsonResponse({'error': 'Отсутствует обязательный параметр product_id'}, status=400)

    try:
        product_id = int(product_id)
    except ValueError:
        return JsonResponse({'error': 'Неверный формат параметра product_id'}, status=400)

    recipes_without_product = Recipe.objects.exclude(
        recipe_product__product=product_id
    ).values('id', 'name').distinct() | Recipe.objects.filter(
        recipe_product__product=product_id,
        recipe_product__weight__lt=10
    ).values('id', 'name').distinct()

    context = {'recipes_without_product': recipes_without_product}
    return render(request, 'cook/show_recipes.html', context)
