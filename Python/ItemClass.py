import random
import string


def generate_code(letters=2, numbers=2) -> str:
    letters = "".join(random.choice(string.ascii_uppercase) for _ in range(letters))
    numbers = "".join(str(random.randint(0, 9)) for _ in range(numbers))
    return letters + numbers


class Item:
    def __init__(self):
        self.code: str = generate_code()
        self.description: str = "-"
        self.quantity: int = random.randint(1, 9)
        self.unit_price_vat_excl: float = float(
            str(random.randint(0, 1000)) + "." + str(random.randint(0, 99))
        )
        self.discount_percent: int = random.randint(0, 50)
        self.discount_absolute: float = round(
            (self.quantity) * (self.discount_percent / 100), 2
        )
        self.discount_reason: str = "-"
        self.price_vat_excl: float = round(self.quantity * self.unit_price_vat_excl, 2)
        self.vat_percent: int = random.randint(16, 22)
        self.vat_absolute: float = round(
            (self.price_vat_excl) * (self.vat_percent / 100), 2
        )
        self.other_taxes: float = 0
        self.total: float = round(
            self.price_vat_excl + self.vat_absolute + self.other_taxes, 2
        )
