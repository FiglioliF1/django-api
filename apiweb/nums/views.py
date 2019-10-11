from django.shortcuts import render
from django.contrib import messages
from nums.models import Numero
from xlrd import open_workbook
import unidecode

# Create your views here.
def carga(request):
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
        try:
            Numero.objects.get_or_create(numero=num,abrev=abrev)
            aux.append(str(num) + " - " + str(abrev))
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
            n = Numero.objects.get(abrev = abrev)
            return render(request,template,{"num":n.numero,"abrev":n.abrev})
        except:
            return render(request,template,{"error":"No encontrado"})
