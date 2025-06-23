from django.urls import path
from .views import dashboard, CreateTransactionView, load_services, booths_dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path(
        "transact/",
        CreateTransactionView.as_view(),
        name="create_transaction",
    ),
    path("load-services/", load_services, name="load_services"),
    path("booths", booths_dashboard, name="booths_dashboard"),
]