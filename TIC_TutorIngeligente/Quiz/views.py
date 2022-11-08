import string
from tkinter.tix import INTEGER
from django.shortcuts import render, redirect, get_object_or_404

from Quiz.sistemafuzzy import sistemaFuzzy

from .forms import RegistroFormulario, UsuarioLoginFormulario

from django.core.exceptions import ValidationError, MultipleObjectsReturned

from .models import QuizUsuario, Pregunta, PreguntasRespondidas, ElegirRespuesta

from django.http import Http404

from django.core.exceptions import ObjectDoesNotExist

array = []
sec = 1800
t_pregunta = 0
ultima = 0
pregunta = None
getP = True
bandera = False

def inicio(request):
	global sec
	sec = 1800
	global t_pregunta
	t_pregunta = 0
	global ultima
	ultima = 0
	global pregunta
	pregunta = None
	global getP
	getP = True
	global bandera
	bandera = False

	context = {

		'bienvenido': 'Bienvenido'

	}

	return render(request, 'inicio.html', context)

def tablero(request):
	total_usaurios_quiz = QuizUsuario.objects.order_by('-puntaje_total')[:10]
	contador = total_usaurios_quiz.count()

	context = {

		'usuario_quiz':total_usaurios_quiz,
		'contar_user':contador
	}

	return render(request, 'play/tablero.html', context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def jugar(request):
	global array
	global sec
	global t_pregunta
	global ultima
	global pregunta
	global getP
	global bandera

	QuizUser, created = QuizUsuario.objects.get_or_create(usuario=get_client_ip(request))

	context = {
				'pregunta':pregunta,
				'array':len(array),
				'sec': sec,
			}

	if request.GET.get('bandera', False):
		bandera = True

	if request.method == 'POST':

		

		pregunta_pk = request.POST.get('pregunta_pk')
		
		
		respuesta_pk = request.POST.get('respuesta_pk')
		print(respuesta_pk)
		
		if respuesta_pk is None:
			return render(request, 'play/jugar.html', context)			

		ultima = t_pregunta
		QuizUser.crear_intentos(pregunta)
		pregunta_respondida = QuizUser.intentos.select_related('pregunta').get(pregunta__pk=pregunta_pk)
		opcion_selecionada = pregunta_respondida.pregunta.opciones.get(pk=respuesta_pk)
		array.append(pregunta_respondida)
		
		calificacion = QuizUser.validar_intento(pregunta_respondida, opcion_selecionada)
		dificultad = pregunta.dificultad

		sistemaFuzzy(calificacion, ultima, bandera, dificultad)
		getP = True
		bandera = False
		return redirect('jugar')

	else:
		if len(array) < 15 and getP == True:
			pregunta = QuizUser.obtener_nuevas_preguntas()
			correcta = obtenerCorrecta(pregunta.id, ElegirRespuesta)
			context = {
				'pregunta':pregunta,
				'array':len(array),
				'sec': sec,
				'correcta': correcta,
			}
			getP = False
		else:
			context = {
				'array':len(array),
				'sec': sec,
				
			}
	
	sec = request.GET.get('sec', None)

	if sec != None:
		t_pregunta = 1800 - int(sec) - ultima
	
	return render(request, 'play/jugar.html', context)

def sinTiempo(request):
	
	return render(request, 'play/sinTiempo.html')

def obtenerCorrecta(pregunta_id, respuesta):
	correcta = respuesta.objects.filter(pregunta=pregunta_id, correcta=True).get()

	return correcta