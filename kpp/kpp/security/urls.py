from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('import/<str:target>', views.import_data, name='import'),
    path('import/<str:target>/<str:parameter>', views.import_data, name='import'),
]