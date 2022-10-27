from email.policy import default
from genericpath import exists
from tabnanny import verbose
from django.db import models
from django.conf import settings

from Quiz.pruebasimpful import sistemaFuzzy
from .sistemafuzzy import obtener_dif_pregunta

import random

class Pregunta(models.Model):

	NUMER_DE_RESPUESTAS_PERMITIDAS = 1

	texto = models.TextField(verbose_name='Texto de la pregunta')
	dificultad = models.IntegerField(verbose_name='Dificultad pregunta', null=True)
	max_puntaje = models.DecimalField(verbose_name='Maximo Puntaje', default=3, decimal_places=2, max_digits=6)
	tipo = models.TextField(verbose_name='Tipo de pregunta')
	unidad = models.IntegerField(verbose_name='Unidad a la que pertenece')

	def __str__(self):
		return self.texto


class ElegirRespuesta(models.Model):

	MAXIMO_RESPUESTA = 3
	MINIMO_RESPUESTA = 2

	pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
	correcta = models.BooleanField(verbose_name='¿Es esta la pregunta correcta?', default=False)
	texto = models.TextField(verbose_name='Texto de la respuesta')
	
	def __str__(self):
		return self.texto

class QuizUsuario(models.Model):
	usuario = models.TextField(verbose_name='Ip usuario')
	puntaje_total = models.DecimalField(verbose_name='Puntaje Total', null=True, default=0.00, decimal_places=2, max_digits=10)

	def crear_intentos(self, pregunta):
		intento = PreguntasRespondidas(pregunta=pregunta, quizUser=self)
		intento.save()

	def obtener_nuevas_preguntas(self):
		dif = obtener_dif_pregunta()
		respondidas = PreguntasRespondidas.objects.filter(quizUser=self).values_list('pregunta__pk', flat=True)
		preguntas_restantes = Pregunta.objects.exclude(pk__in=respondidas)
		if not preguntas_restantes.exists():
			return None
		try: 
			return random.choice(preguntas_restantes.filter(dificultad=dif))
		except IndexError:
			return random.choice(preguntas_restantes)

	def validar_intento(self, pregunta_respondida, respuesta_selecionada):
		if pregunta_respondida.pregunta_id != respuesta_selecionada.pregunta_id:
			return

		pregunta_respondida.respuesta_selecionada = respuesta_selecionada
		if pregunta_respondida.respuesta_selecionada is None:
			print("None")
			
		if respuesta_selecionada.correcta is True:
			pregunta_respondida.correcta = True
			pregunta_respondida.puntaje_obtenido = respuesta_selecionada.pregunta.max_puntaje
			pregunta_respondida.respuesta = respuesta_selecionada
			calificacion = 1

		else:
			pregunta_respondida.respuesta = respuesta_selecionada
			calificacion = 0

		pregunta_respondida.save()
		
		self.actualizar_puntaje()

		return calificacion

	def actualizar_puntaje(self):
		puntaje_actualizado = self.intentos.filter(correcta=True).aggregate(
			models.Sum('puntaje_obtenido'))['puntaje_obtenido__sum']

		self.puntaje_total = puntaje_actualizado
		self.save()

class PreguntasRespondidas(models.Model):
	quizUser = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE, related_name='intentos')
	pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
	respuesta = models.ForeignKey(ElegirRespuesta, on_delete=models.CASCADE, null=True)
	correcta  = models.BooleanField(verbose_name='¿Es esta la respuesta correcta?', default=False)
	puntaje_obtenido = models.DecimalField(verbose_name='Puntaje Obtenido', default=0, decimal_places=2, max_digits=6)
