from django.urls import path

from .views import (
			inicio,
			jugar,
			sinTiempo,
			tablero,
			sinTiempo)

urlpatterns = [
	
	path('inicio/', inicio, name='inicio'),
	path('tablero/', tablero, name='tablero'),
	path('jugar/', jugar, name='jugar'),
	path('sinTiempo/', sinTiempo, name='sinTiempo'),

]