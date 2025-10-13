from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Location
from .services.openweather import OpenWeatherClient
from .forms import SignUpForm

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "weatherapp/index.html"

    def get(self, request, *args, **kwargs):
        client = OpenWeatherClient()
        locations = request.user.locations.all()
        weather_data = []
        for loc in locations:
            try:
                weather = client.get_weather(float(loc.latitude), float(loc.longitude))
                temp = weather.get("main", {}).get("temp")
            except Exception:
                temp = None
            weather_data.append({
                "id": loc.id,
                "name": loc.name,
                "temp": temp,
            })
        return render(request, self.template_name, {"weather_data": weather_data})

class SearchResultsView(LoginRequiredMixin, TemplateView):
    template_name = "weatherapp/search_results.html"

    def get(self, request, *args, **kwargs):
        q = request.GET.get("q", "")
        results = []
        if q:
            client = OpenWeatherClient()
            try:
                results = client.search_locations(q)
            except Exception:
                results = []
        return render(request, self.template_name, {"q": q, "results": results})

class AddLocationView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        lat = request.POST.get("lat")
        lon = request.POST.get("lon")
        if not (name and lat and lon):
            return redirect("index")
        Location.objects.create(user=request.user, name=name, latitude=lat, longitude=lon)
        return redirect("index")

class DeleteLocationView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        loc = get_object_or_404(Location, pk=pk, user=request.user)
        loc.delete()
        return redirect("index")

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
