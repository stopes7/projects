from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Quote
from .utils import get_random_quote
from .forms import QuoteForm

def random_quote(request):
    quote = get_random_quote()
    if quote:
        # атомарно увеличиваем views через F
        Quote.objects.filter(pk=quote.pk).update(views=F("views") + 1)
        # обновим в объекте текущее значение views (чтобы шаблон сразу видел)
        quote.refresh_from_db()
    return render(request, "quotes/random_quote.html", {"quote": quote})

@require_POST
def like_quote(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    Quote.objects.filter(pk=pk).update(likes=F("likes") + 1)
    quote.refresh_from_db()
    return JsonResponse({"likes": quote.likes})

@require_POST
def dislike_quote(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    Quote.objects.filter(pk=pk).update(dislikes=F("dislikes") + 1)
    quote.refresh_from_db()
    return JsonResponse({"dislikes": quote.dislikes})

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