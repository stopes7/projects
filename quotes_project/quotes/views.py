from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F
from .models import Quote
from .utils import get_random_quote
from .forms import QuoteForm

def random_quote(request):
    # Обработка POST (лайк/дизлайк) — сначала обрабатываем POST, чтобы не менять views
    if request.method == "POST":
        quote_id = request.POST.get("quote_id")
        if quote_id:
            try:
                q = Quote.objects.get(pk=quote_id)
            except Quote.DoesNotExist:
                return redirect("random_quote")
            if "like" in request.POST:
                Quote.objects.filter(pk=q.pk).update(likes=F("likes") + 1)
            elif "dislike" in request.POST:
                Quote.objects.filter(pk=q.pk).update(dislikes=F("dislikes") + 1)
        # После обработки POST — редирект на GET (чтобы избежать повторной отправки формы)
        return redirect("random_quote")

    # GET — выбираем случайную цитату и увеличиваем views
    quote = get_random_quote()
    if quote:
        Quote.objects.filter(pk=quote.pk).update(views=F("views") + 1)
        quote.refresh_from_db()

    return render(request, "quotes/random_quote.html", {"quote": quote})

def top_quotes(request):
    quotes = Quote.objects.order_by("-likes", "-views")[:10]
    return render(request, "quotes/top_quotes.html", {"quotes": quotes})

def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect("random_quote")
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})


def dashboard(request):
    quotes = Quote.objects.all()
    sources = [q.source for q in quotes]
    likes = [q.likes for q in quotes]
    views = [q.views for q in quotes]
    return render(request, "quotes/dashboard.html", {
        "sources": sources,
        "likes": likes,
        "views": views,
    })