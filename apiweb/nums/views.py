from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from nums.models import Numero, Log
from rest_framework.response import Response
from django.http import HttpResponse
from xlrd import open_workbook
import unidecode


# Create your views here.
@login_required
def add(request):
    if request.method == 'GET':
        ind = 1
        for it in Numero.objects.all():
            if ind != it.num_id:
                break
            ind = ind + 1
        return HttpResponse(ind)

@login_required
def delete(request):
    num_id = request.POST.get('num_id')
    obj = Numero.objects.get(num_id=num_id)
    log = Log.objects.create(usuario=request.user.username,tipo="Eliminación",numero_viejo=getattr(obj,'numero'),abrev_viejo=getattr(obj,'abrev'),numero_nuevo="-",abrev_nuevo="-")
    obj.delete()
    log.save()
    return HttpResponse("Eliminado")

@login_required
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
    #Chequeo si el nuevo número o abreviación ya existen
    aux = Numero.objects.filter(numero=num)
    for i in aux:
        if str(i.num_id) != str(num_id):
            return HttpResponse("Ese número ya está en uso")
    aux = Numero.objects.filter(abrev=abrev)
    for i in aux:
        if str(i.num_id) != str(num_id):
            return HttpResponse("Esa abreviación ya está en uso")

    #Si recibo un num_id que no existe, siginifica que lo tengo que agregar
    aux = Numero.objects.filter(num_id=num_id)
    aux1 = '0'
    if not aux:
        aux1 = abrev
        if abrev.startswith('*'):
            aux1 = aux1[1:]
        else:
            abrev = "*" + abrev
        print("Se crea: numero: " + num + " abrev: " + abrev)
        if aux1.isnumeric():
            ob = Numero.objects.create(num_id=num_id,numero=num,abrev=abrev)
            ob.save()
            log = Log.objects.create(usuario=request.user.username,tipo="Creación",numero_viejo="-",abrev_viejo="-",numero_nuevo=num,abrev_nuevo=abrev)
            return HttpResponse("Creado")
        else:
            return HttpResponse("Caracteres inaceptables")

    obj = Numero.objects.get(num_id=num_id)
    n_viejo = obj.numero
    a_viejo = obj.abrev
    obj.numero = num
    obj.abrev = abrev
    print("Modificado - ID: " + str(obj.num_id)+ " -> Num: " + str(obj.numero) + " - Abrev: " + str(abrev))
    obj.save()
    log = Log.objects.create(usuario=request.user.username,tipo="Edición",numero_viejo=n_viejo,abrev_viejo=a_viejo,numero_nuevo=num,abrev_nuevo=abrev)
    return HttpResponse("Actualizado")

@login_required
def load(request):
    template = "carga.html"
    if request.method == 'GET':
        return render(request, template, {})
    data = request.FILES['file']

    if not data.name.endswith('.ods') and not data.name.endswith('.xlsx') and not data.name.endswith('.xls'):
        return render(request, template, {"error":"No es una planilla de cálculo soportada (.ods, .xls, .xlsx)"})

    documento = open_workbook(data.name, file_contents=data.read())
    hoja = documento.sheet_by_index(0)
    filas = hoja.nrows
    aux = []
    ids = []
    for it in Numero.objects.all():
        ids.append(it.num_id)
    for i in range(filas):
        num = unidecode.unidecode(str(hoja.cell_value(i,0)))
        abrev = unidecode.unidecode(str(hoja.cell_value(i,1)))
        if not num.isnumeric():
            continue
        try:
            obj = Numero.objects.get(numero=num)
            print("Ya existe: " + str(num))
        except:
            try:
                obj = Numero.objects.get(abrev=abrev)
                print("Ya existe: " + str(num))
            except:
                i = 1
                while i in ids:
                    i = i +1
                ob = Numero.objects.create(num_id=i,numero=num,abrev=abrev)
                ob.save()
                log = Log.objects.create(usuario=request.user.username,tipo="Creación",numero_viejo="-",abrev_viejo="-",numero_nuevo=num,abrev_nuevo=abrev)
                ids.append(i)
                print("Guardado: " + str(num))
                aux.append(tuple([str(num),str(abrev)]))
    return render(request, 'carga.html', {"data":aux})

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
