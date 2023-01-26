from django.urls import path
from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import *

from .forms import ElegirInlineFormset

class ElegirRespuestaInline(admin.TabularInline):
	model = ElegirRespuesta
	can_delete =False
	max_num = ElegirRespuesta.MAXIMO_RESPUESTA
	min_num = ElegirRespuesta.MINIMO_RESPUESTA
	formset = ElegirInlineFormset

class PreguntaAdmin(admin.ModelAdmin):
	change_list_template = 'pregunta_changelist.html'
	model = Pregunta
	inlines = (ElegirRespuestaInline, )
	list_display = ['texto',]
	search_fields = ['texto', 'preguntas__texto']
	
	def get_urls(self):
		urls = super().get_urls()
		my_urls = [ 
			path('bimestre_1_activo/', self.activar_b1),
			path('bimestre_2_activo/', self.activar_b2),
			]
		return my_urls + urls 

	def activar_b1(self, request):
		for i in range(1, 5):
			self.model.objects.filter(unidad=i).update(bimestre_activo=True)

		for i in range(5, 7):
			self.model.objects.filter(unidad=i).update(bimestre_activo=False)
		self.message_user(request, "Las preguntas del bimestre 1 están activas")
		return HttpResponseRedirect("../") 

	def activar_b2(self, request):
		for i in range(1, 5):
			self.model.objects.filter(unidad=i).update(bimestre_activo=False)

		for i in range(5, 7):
			self.model.objects.filter(unidad=i).update(bimestre_activo=True)
		self.message_user(request, "Las preguntas del bimestre 2 están activas")
		return HttpResponseRedirect("../")


class PreguntasRespondidasAdmin(admin.ModelAdmin):
	list_display = ['pregunta', 'respuesta', 'correcta', 'puntaje_obtenido']

	class Meta:
		model = PreguntasRespondidas


admin.site.register(PreguntasRespondidas)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(ElegirRespuesta)
admin.site.register(QuizUsuario)
admin.site.register(ComentarioUsuario)