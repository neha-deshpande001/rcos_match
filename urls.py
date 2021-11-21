from django.urls import path

from . import views

app_name = 'rcos_match'

urlpatterns = [
    path('matching/<int:pk>/<int:match_index>/', views.Match_View.as_view(), name='matching'),
    path('table/<int:pk>', views.Table_View.as_view(), name='seek table')
]
