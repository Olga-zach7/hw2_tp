class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity
    @quantity.setter
    def quantity(self, value):
        value = float(value)
        if value<=0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"
    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return NotImplemented
        return self.name==other.name and self.unit==other.unit
    

class Recipe:
    def __init__(self, title: str, ingredients: list = None):
        self.title = title
        self.ingredients: list[Ingredient] = []
        if ingredients:
            for ing in ingredients:
                self.add_ingredient(ing)


    def add_ingredient(self, ingredient: Ingredient):
        for existing in self.ingredients:
            if existing == ingredient:
                existing.quantity += ingredient.quantity
                return
        self.ingredients.append(Ingredient(ingredient.name, ingredient.quantity, ingredient.unit))

    @staticmethod
    def is_valid_ratio(ratio):
        try:
            return float(ratio) > 0
        except (TypeError, ValueError):
            return False

    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент масштабирования должен быть больше нуля")
        new_recipe = Recipe(self.title)
        for ing in self.ingredients:
            new_recipe.ingredients.append(Ingredient(ing.name, ing.quantity * float(ratio), ing.unit))
        return new_recipe

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        lines = [f"Рецепт: {self.title}"]
        for ing in self.ingredients:
            lines.append(f"  - {ing}")
        return "\n".join(lines)
    

class ShoppingList:
    def __init__(self):
        self._items: list[tuple[Ingredient, str]] = []
    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled = recipe.scale(portions)
        for ing in scaled.ingredients:
            self._items.append((ing, recipe.title))

    def remove_recipe(self, title: str):
        self._items = [(ing, t) for ing, t in self._items if t != title]
    def get_list(self):
        totals: dict[tuple[str, str], float] = {}
        for ing, i in self._items:
            key = (ing.name, ing.unit)
            totals[key] = totals.get(key, 0.0) + ing.quantity
        result = [Ingredient(name, qty, unit) for (name, unit), qty in totals.items()]
        result.sort(key=lambda i: i.name)
        return result

    def __add__(self, other: "ShoppingList"):
        if not isinstance(other, ShoppingList):
            return NotImplemented
        new_list = ShoppingList()
        new_list._items = self._items.copy() + other._items.copy()
        return new_list
    

class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients: list = None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float):
        base = super().scale(ratio)
        new_recipe = DietaryRecipe(self.title, self.diet_type)
        new_recipe.ingredients = base.ingredients
        return new_recipe

    def __str__(self):
        base_str = super().__str__()
        lines = base_str.split("\n")
        lines[0] = f"[{self.diet_type}] {lines[0].replace('Рецепт: ', 'Рецепт: ')}"
        lines[0] = f"Рецепт: [{self.diet_type}] {self.title}"
        return "\n".join(lines)