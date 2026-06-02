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