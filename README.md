# Система управления рецептами

Консольное приложение для создания блюд, управления рецептами, масштабирования порций и генерации списка покупок.

## Установка

```bash
git clone https://github.com/Olga-zach7/hw2_tp
cd hw2_tp
pip install -r requirements.txt
```

## Использование

```python
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe

# Создание ингредиентов
potato = Ingredient("Картофель", 300, "г")
onion = Ingredient("Лук", 150, "г")

# Создание рецепта
soup = Recipe("Куриный суп")
soup.add_ingredient(potato)
soup.add_ingredient(onion)

# Масштабирование на 2 порции
soup_x2 = soup.scale(2)

# Список покупок
sl = ShoppingList()
sl.add_recipe(soup, 3)
for item in sl.get_list():
    print(item)

# Диетический рецепт
vegan_soup = DietaryRecipe("Овощной суп", "веган")
vegan_soup.add_ingredient(potato)
print(vegan_soup)
```

## Запуск тестов

```bash
pytest
```

с подробным выводом:

```bash
pytest -v
```

## Автор

ФИО: Зачиняева Ольга Евгеньевна  
Учебная группа: ББИ2505