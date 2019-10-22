from django.shortcuts import render
from django.contrib import messages
from nums.models import Numero
from rest_framework.response import Response
from django.http import HttpResponse
from xlrd import open_workbook
import unidecode

# Create your views here.
def delete(request):
    num_id = request.POST.get('num_id')
    obj = Numero.objects.get(num_id=num_id)
    obj.delete()
    return HttpResponse("Eliminado")

def edit(request):
    template = "editar.html"
    nums = []
    for i in Numero.objects.all():
        if i.numero.isnumeric():
            nums.append(tuple([str(i.num_id),str(i.numero),str(i.abrev)]))
    if request.method == 'GET':
        return render(request, template, {"nums":nums})
    num_id = request.POST.get('num_id')
    num = request.POST.get('num')
    abrev = request.POST.get('abrev')
    obj = Numero.objects.get(num_id=num_id)
    obj.numero = num
    obj.abrev = abrev
    print("id: " + str(obj.num_id)+ " - Num: " + str(obj.numero) + " - Abrev: " + str(abrev))
    obj.save()
    return HttpResponse("Actualizado")

def load(request):
    template = "formulario.html"
    if request.method == 'GET':
        return render(request, template, {})
    data = request.FILES['file']

    if not data.name.endswith('.csv') and not data.name.endswith('.xlsx') and not data.name.endswith('.xls'):
        return render(request, template, {"error":"No es una planilla de cálculo"})

    documento = open_workbook(data.name, file_contents=data.read())
    hoja = documento.sheet_by_index(0)
    filas = hoja.nrows
    aux = []

    for i in range(filas):
        num = unidecode.unidecode(str(hoja.cell_value(i,0)))
        abrev = unidecode.unidecode(str(hoja.cell_value(i,1)))
        if not num.isnumeric():
            continue
        try:
            Numero.objects.get_or_create(numero=num,abrev=abrev)
            aux.append(tuple([str(num),str(abrev)]))
            print(str(i) + ") Entrada creada (" + str(num) + " - " + str(abrev) + ")")
        except:
            print("Error con la linea: " + str(i))
    return render(request, 'formulario.html', {"data":aux})

def index(request):
    template = "index.html"
    if request.method == 'GET':
        return render(request, template, {})

    numero = request.GET.get("numero",request.POST.get('numero'))
    abrev = request.GET.get("abrev",request.POST.get('abreviacion'))
    if numero != "":
        try:
            n = Numero.objects.get(numero=numero)
            return render(request,template,{"num":n.numero,"abrev":n.abrev})
        except:
            return render(request,template,{"error":"No encontrado"})
    else:
        try:
            if not abrev.startswith("*"):
                abrev = "*" + abrev
            n = Numero.objects.get(abrev = abrev)
            return render(request,template,{"num":n.numero,"abrev":n.abrev})
        except:
            return render(request,template,{"error":"No encontrado"})
