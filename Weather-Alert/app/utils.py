def format_city(city: str) -> str:
    if not city:
        return ""
    return city.strip().title()


def is_valid_city(city: str) -> bool:
    return bool(city and city.strip())