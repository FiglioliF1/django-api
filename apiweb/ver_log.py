from nums.models import Log
objs = Log.objects.all()
ind = 0
for it in objs:
     if ind==0:
             print("|   usuario  |    tipo     |    num_viejo   | abr_vieja|    num_nuevo   | abr_nueva|    hora  |")
             ind = ind + 1
             continue
     print("| " + it.usuario,end='')
     for i in range(11 - len(it.usuario)):
         print(" ",end='')
     print("| " + it.tipo,end='')
     for i in range(12 - len(it.tipo)):
         print(" ",end='')
     print("| " + it.numero_viejo,end='')
     for i in range(15 - len(it.numero_viejo)):
         print(" ",end='')
     print("| " + it.abrev_viejo,end='')
     for i in range(9 - len(it.abrev_viejo)):
         print(" ",end='')
     print("| " + it.numero_nuevo,end='')
     for i in range(15 - len(it.numero_nuevo)):
         print(" ",end='')
     print("| " + it.abrev_nuevo,end='')
     for i in range(9 - len(it.abrev_nuevo)):
         print(" ",end='')
     print("| " + str(it.hora)[:22] + " |")
