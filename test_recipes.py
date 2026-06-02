import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe

class TestIngredient:
    def test_init_correct_attributes(self):
        ing = Ingredient("Рис", 500, "г")
        assert ing.name == "Рис"
        assert ing.quantity == 500.0
        assert ing.unit == "г"
    def test_quantity_is_float(self):
        ing = Ingredient("Гречка", 200, "г")
        assert isinstance(ing.quantity, float)
    def test_quantity_setter_positive(self):
        ing = Ingredient("Сливочное масло", 100, "г")
        ing.quantity = 50
        assert ing.quantity == 50.0
    def test_quantity_setter_raises_on_zero(self):
        with pytest.raises(ValueError, match="Количество должно быть положительным"):
            Ingredient("Морская соль", 0, "г")
    def test_quantity_setter_raises_on_negative(self):
        with pytest.raises(ValueError, match="Количество должно быть положительным"):
            Ingredient("Морская соль", -1, "г")
    def test_str(self):
        ing = Ingredient("Рис", 500, "г")
        assert str(ing) == "Рис: 500.0 г"
    def test_repr(self):
        ing = Ingredient("Рис", 500, "г")
        assert repr(ing) == "Ingredient('Рис', 500.0, 'г')"
    def test_eq_same_name_and_unit(self):
        ing1 = Ingredient("Рис", 100, "г")
        ing2 = Ingredient("Рис", 500, "г")
        assert ing1 == ing2
    def test_eq_different_name(self):
        ing1 = Ingredient("Рис", 100, "г")
        ing2 = Ingredient("Булгур", 100, "г")
        assert ing1 != ing2
    def test_eq_different_unit(self):
        ing1 = Ingredient("Кефир", 500, "мл")
        ing2 = Ingredient("Кефир", 500, "г")
        assert ing1 != ing2


class TestRecipe:
    def test_init_empty(self):
        recipe = Recipe("Овощное рагу")
        assert recipe.title == "Овощное рагу"
        assert recipe.ingredients == []
    def test_init_with_ingredients(self):
        ings = [Ingredient("Картофель", 300, "г"), Ingredient("Морковь", 200, "г")]
        recipe = Recipe("Домашний гарнир", ings)
        assert len(recipe) == 2
    def test_add_ingredient_new(self):
        recipe = Recipe("Овощное рагу")
        recipe.add_ingredient(Ingredient("Картофель", 300, "г"))
        assert len(recipe) == 1
    def test_add_ingredient_duplicate_sums_quantity(self):
        recipe = Recipe("Овощное рагу")
        recipe.add_ingredient(Ingredient("Картофель", 300, "г"))
        recipe.add_ingredient(Ingredient("Картофель", 200, "г"))
        assert len(recipe) == 1
        assert recipe.ingredients[0].quantity == 500.0
    def test_add_ingredient_different_unit_not_duplicate(self):
        recipe = Recipe("Овощное рагу")
        recipe.add_ingredient(Ingredient("Сметана", 200, "мл"))
        recipe.add_ingredient(Ingredient("Сметана", 100, "г"))
        assert len(recipe) == 2
    def test_scale_returns_new_object(self):
        recipe = Recipe("Овощное рагу")
        recipe.add_ingredient(Ingredient("Картофель", 300, "г"))
        scaled = recipe.scale(2)
        assert scaled is not recipe
    def test_scale_multiplies_quantity(self):
        recipe = Recipe("Овощное рагу")
        recipe.add_ingredient(Ingredient("Картофель", 300, "г"))
        scaled = recipe.scale(2)
        assert scaled.ingredients[0].quantity == 600.0
    def test_scale_original_unchanged(self):
        recipe = Recipe("Овощное рагу")
        recipe.add_ingredient(Ingredient("Картофель", 300, "г"))
        recipe.scale(3)
        assert recipe.ingredients[0].quantity == 300.0
    def test_scale_raises_on_zero(self):
        recipe = Recipe("Овощное рагу")
        with pytest.raises(ValueError):
            recipe.scale(0)
    def test_scale_raises_on_negative(self):
        recipe = Recipe("Овощное рагу")
        with pytest.raises(ValueError):
            recipe.scale(-1)
    def test_len(self):
        recipe = Recipe("Овощное рагу")
        recipe.add_ingredient(Ingredient("Картофель", 300, "г"))
        recipe.add_ingredient(Ingredient("Морковь", 200, "г"))
        assert len(recipe) == 2
    def test_is_valid_ratio_true(self):
        assert Recipe.is_valid_ratio(1.5) is True
        assert Recipe.is_valid_ratio(1) is True
    def test_is_valid_ratio_false(self):
        assert Recipe.is_valid_ratio(0) is False
        assert Recipe.is_valid_ratio(-1) is False
        assert Recipe.is_valid_ratio("abc") is False
        assert Recipe.is_valid_ratio(None) is False


class TestShoppingList:
    def _make_pizza(self):
        r = Recipe("Куриный суп")
        r.add_ingredient(Ingredient("Картофель", 300, "г"))
        r.add_ingredient(Ingredient("Лук", 150, "г"))
        return r
    def _make_pasta(self):
        r = Recipe("Омлет")
        r.add_ingredient(Ingredient("Картофель", 200, "г"))
        r.add_ingredient(Ingredient("Яйца", 2, "шт"))
        return r
    def test_add_recipe_adds_ingredients(self):
        sl = ShoppingList()
        sl.add_recipe(self._make_pizza(), 1)
        items = sl.get_list()
        names = [i.name for i in items]
        assert "Картофель" in names
        assert "Лук" in names
    def test_add_recipe_scales_portions(self):
        sl = ShoppingList()
        sl.add_recipe(self._make_pizza(), 2)
        items = {i.name: i.quantity for i in sl.get_list()}
        assert items["Картофель"] == 600.0
        assert items["Лук"] == 300.0
    def test_add_recipe_raises_on_zero_portions(self):
        sl = ShoppingList()
        with pytest.raises(ValueError, match="Количество порций должно быть положительным"):
            sl.add_recipe(self._make_pizza(), 0)
    def test_add_recipe_raises_on_negative_portions(self):
        sl = ShoppingList()
        with pytest.raises(ValueError):
            sl.add_recipe(self._make_pizza(), -1)
    def test_remove_recipe_removes_correct_items(self):
        sl = ShoppingList()
        sl.add_recipe(self._make_pizza(), 1)
        sl.add_recipe(self._make_pasta(), 1)
        sl.remove_recipe("Куриный суп")
        names = [i.name for i in sl.get_list()]
        assert "Лук" not in names
        assert "Яйца" in names
    def test_remove_recipe_nonexistent_no_error(self):
        sl = ShoppingList()
        sl.add_recipe(self._make_pizza(), 1)
        sl.remove_recipe("Несуществующий рецепт")
        assert len(sl.get_list()) == 2
    def test_get_list_sums_same_ingredients(self):
        sl = ShoppingList()
        sl.add_recipe(self._make_pizza(), 1)
        sl.add_recipe(self._make_pasta(), 1)
        items = {i.name: i.quantity for i in sl.get_list()}
        assert items["Картофель"] == 500.0
    def test_get_list_sorted_by_name(self):
        sl = ShoppingList()
        sl.add_recipe(self._make_pizza(), 1)
        sl.add_recipe(self._make_pasta(), 1)
        names = [i.name for i in sl.get_list()]
        assert names == sorted(names)
    def test_add_two_shopping_lists(self):
        sl1 = ShoppingList()
        sl1.add_recipe(self._make_pizza(), 1)
        sl2 = ShoppingList()
        sl2.add_recipe(self._make_pasta(), 1)
        combined = sl1 + sl2
        names = [i.name for i in combined.get_list()]
        assert "Картофель" in names
        assert "Лук" in names
        assert "Яйца" in names
    def test_add_does_not_mutate_originals(self):
        sl1 = ShoppingList()
        sl1.add_recipe(self._make_pizza(), 1)
        original_len = len(sl1._items)
        sl2 = ShoppingList()
        sl2.add_recipe(self._make_pasta(), 1)
        sl1 + sl2
        assert len(sl1._items) == original_len