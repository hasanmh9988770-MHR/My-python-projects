def list_hotels(hotels):
    return "\n".join(str(h) for h in hotels)


def sort_by_name(hotels):
    return "\n".join(str(h) for h in sorted(hotels, key=lambda x: x.name))


def sort_by_rating(hotels):
    return "\n".join(str(h) for h in sorted(hotels, key=lambda x: x.rating, reverse=True))


def sort_by_rooms(hotels):
    return "\n".join(str(h) for h in sorted(hotels, key=lambda x: x.rooms, reverse=True))


def filter_city(city, hotels):
    data = [h for h in hotels if h.location.lower() == city.lower()]
    return "\n".join(str(h) for h in data) if data else "No hotels found"


def list_users(users):
    return "\n".join(str(u) for u in users)


def book_hotel(name, hotels):
    for h in hotels:
        if h.name.lower() == name.lower():
            return h.book()
    return "Hotel not found"