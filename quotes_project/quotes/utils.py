import random
from .models import Quote

def get_random_quote():
    """
    Возвращает одну Quote с учётом веса.
    Если нет ни одной цитаты — возвращает None.
    """
    qs = list(Quote.objects.all())
    if not qs:
        return None
    weights = [q.weight if q.weight > 0 else 1 for q in qs]
    return random.choices(qs, weights=weights, k=1)[0]