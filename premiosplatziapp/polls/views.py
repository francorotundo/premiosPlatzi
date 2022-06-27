from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect 
from django.views import generic #esta nos permite instaciar nuestras vistas basadas en clases
from django.utils import timezone

from .models import Question, Choice

# def index(request):
#     latest_question_list = Question.objects.all()
#     return render(request, "polls/index.html", {
#         "latest_question_list": latest_question_list
#         })


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {
#         "question": question
#         })


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html",{
#         "question": question
#     })

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published question"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5] #order_by se utiliza para ordenar se coloca un - para organizar de forma descendente y para traer cierta cantidad de resultados se utiliza los slices en este caso los primeros 5 valores generados por el order_by [:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def  get_queryset(self):
        """Excludes any questions that aren't published yet"""
        return Question.objects.filter(pub_date__lte=timezone.now())



class ResultsView(DetailView):
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"]) #request.POST["name en el input del formulario"] de esta forma traemos la información para que pueda ser utilizada .
        
    except (KeyError, Choice.DoesNotExist): #KeyError es para cuando el usuarion no escoge una opción y choise.DoesNotExist es para cuando la opción seleciona no exite.
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "No elegiste una respuesta"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,))) #aquí se redirecciona la pag a results organizando en orden descendente las diferentes opciones 