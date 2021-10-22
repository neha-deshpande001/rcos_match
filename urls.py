from django.urls import path

from . import views

app_name = 'rcos_match'

urlpatterns = [
    path('matching/<int:individual_id>/<int:match_index>/', views.matching, name='matching'),
    path('matching/<int:individual_id>/<int:match_index>/submit',
         views.matching_submit, name='matching submit'),
    path('table/<int:individual_id>', views.table, name="seek_table")
]
