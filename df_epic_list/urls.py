from django.urls import path
from df_epic_list import views

urlpatterns = [
    path('quantity/', views.EpicList.as_view())
]
