from django.urls import path
from ledgers.views import LedgerView, DetailView

urlpatterns = [
    path('', LedgerView.as_view()),
    path('/<int:post_id>', DetailView.as_view()),
]