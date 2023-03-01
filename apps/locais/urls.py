from django.urls import path, reverse_lazy
from .views import LocalListView

app_name = "locais"

urlpatterns = [
    path('lojas/', LocalListView.as_view(), name='lojas'),
]
