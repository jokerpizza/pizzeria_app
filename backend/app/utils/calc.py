def convert_to_kg(amount: float, unit: str) -> float:
    if unit == "kg":
        return amount
    if unit == "g":
        return amount / 1000
    if unit == "l":
        # treat liter same as kg for price (assumption)
        return amount
    if unit == "ml":
        return amount / 1000
    if unit == "szt":
        # szt uses price_per_kg as price per szt (convention)
        return amount
    raise ValueError("Unknown unit")

def convert_between(amount: float, from_u: str, to_u: str) -> float:
    # only need when echoing amounts
    kg = convert_to_kg(amount, from_u)
    if to_u == "kg":
        return kg
    if to_u == "g":
        return kg * 1000
    if to_u == "l":
        return kg
    if to_u == "ml":
        return kg * 1000
    if to_u == "szt":
        return kg
    raise ValueError("Unknown unit")
