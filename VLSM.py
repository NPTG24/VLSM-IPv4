result = []

def datosp():
    IPinicial = []
    host = []
    print("Ingrese IP inicial")
    for i in range(4):
        correct = False
        while(not correct):
            try:
                inicial = (input(f"Ingrese octeto {i+1}: "))
                if (int(inicial) >= 0):
                    correct = True
                    IPinicial.append(inicial)
                else:
                    print("\nIngrese un valor correcto. Vuelva a intentarlo...\n")
            except (RuntimeError, TypeError, NameError, IndexError, ValueError):
                print("\nIngrese un valor correcto. Vuelva a intentarlo...\n")
                
    correct = False
    while(not correct):
        try:
            prefijo = int(input("Ingrese mascara inicial(prefijo): "))
            if prefijo > 0:
                correct = True
            else:
                print("\nIngrese un valor correcto. Vuelva a intentarlo...\n")
        except (RuntimeError, TypeError, NameError, IndexError, ValueError):
            print("\nIngrese un valor correcto. Vuelva a intentarlo...\n")        
    print("IP guardada....")
    print(".".join(IPinicial),"/",prefijo)
    bin(prefijo)
    print('\n')

    correct = False
    while(not correct):
        try:
            j = int(input("Cuantos hosts desea ingresar: "))
            if j > 0:
                correct = True
            else:
                print("\nIngrese un valor correcto. Vuelva a intentarlo...\n")
        except (RuntimeError, TypeError, NameError, IndexError, ValueError):
            print("\nIngrese un valor correcto. Vuelva a intentarlo...\n")

    for i in range(j):
        correct = False
        while(not correct):
            try:
                h = int(input(f"Host {i+1}: "))
                if h >= 0:
                    correct = True
                    host.append(h)
                else:
                    print("\nIngrese un valor correcto. Vuelva a intentarlo...\n")
            except (RuntimeError, TypeError, NameError, IndexError, ValueError):
                print("\nIngrese un valor correcto. Vuelva a intentarlo...\n")                

    host.sort(reverse=True)
    print("Ordenando de mayor a menor quedaría de la siguiente forma....")
    print(host)
    tabla()
    result.clear()
    calculos(host, IPinicial, prefijo)

def tabla():
    o = '0.240'
    Lista = [[' IP', .128, .192, .224, o, .248, .252, .254], [' Red', 2, 4, 8, 16, 32, 64, 128],
             [' Host', 128, 64, 32, 16, 8, 4, 2]]
    print("\n")
    print("                                  ***TABLA DE AYUDA***")
    Tabla = """\
+-------------------------------------------------------------------------------------+
|  Prefijo     /25        /26        /27        /28        /29        /30        /31  |
|-------------------------------------------------------------------------------------|
{}
+-------------------------------------------------------------------------------------+\
"""
    Tabla = (Tabla.format('\n'.join("| {:<10} {:>5} {:>10} {:>10} {:>10} {:>10} {:>10} {:>11} |".format(*fila) for fila in Lista)))
    print(Tabla)
    print("\n")

def bin(prefijo):
    binario = []
    imprimir = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    c = 1
    for i in range(4):
        binario.append([])
        for j in range(8):
            if(c <= prefijo):
                binario[i].append(1)
                c+=1
            else:
                binario[i].append(0)
    c = 1
    for k in range(32):
        if(c <= prefijo):
            imprimir[k] = 1
            c+=1

    print("Binario del prefijo:", *imprimir, sep=" ")
    bindec(binario)


def bindec(binario):
    n = 0
    for j in range(len(binario)+4):
        if binario[0][j] == 1:
            n += pow(2, 7-j)
    result.append(n)

    n = 0
    for j in range(len(binario)+4):
        if binario[1][j] == 1:
            n += pow(2, 7-j)
    result.append(n)

    n = 0
    for j in range(len(binario)+4):
        if binario[2][j] == 1:
            n += pow(2, 7-j)
    result.append(n)

    n = 0
    for j in range(len(binario)+4):
        if binario[3][j] == 1:
            n += pow(2, 7-j)
    result.append(n)

    print("Conversión de binario a decimal(máscara de red): ", end="")
    print(*result, sep=".")

def calculos(host, IPinicial, prefijo):
    IP = [8192,4096,2048,1024,512,256,128,64,32,16,8,4,2] #host = [80, 60, 20, 2, 2, 2]
    hm = []
    exp = []
    nuevo = []
    c = 0
    for i in range(len(host)):
        for j in range(len(IP)):
            if IP[j] > host[i]:
                x = pow(2, 13 - j) - 2
                e = 13-j
        hm.append(x)
        exp.append(e)

    for i in range(len(exp)):
        result.clear()
        ceros = 32-prefijo 
        print(f"Para {host[i]} hosts necesito {exp[i]} bits")
        print(f"Los hosts máximos serían: 2^{exp[i]} - 2 (red inicial y broadcast) = ", hm[i])
        print("Su dirección inicial es: ", end ="")
        IPinicial[3] = int(IPinicial[3]) + int(c)
        if IPinicial[3] == 256:
            nuevo = IPinicial[:]
            nuevo[2] = int(nuevo[2]) + int(1)
            nuevo[3] = 0
            print(*nuevo, sep =".")
        else:
            print(*IPinicial, sep =".")
        t = ceros-exp[i]+prefijo
        
        print(f"el prefijo de la máscara es: {ceros} - {exp[i]} + {prefijo} = {t} ")
        bin(t)
        print("Su rango de direcciones válido es: ", end ="")
        IPinicial[3] = int(IPinicial[3]) + int(1)
        if IPinicial[3] > 255:
            IPinicial[3] = 1
            IPinicial[2] = int(IPinicial[2]) + int(1)
            print(*IPinicial, sep =".", end="")
        elif IPinicial[3] < 256:
            print(*IPinicial, sep =".", end="")
    
        IPinicial[3] = int(IPinicial[3]) + int(hm[i]) - int(1)    
          
        if IPinicial[3] > 254:
            IPinicial[3] = 254
            print(" - ", end="")
            if result[3] > 0:
                IPinicial[3] = int(255) - int(result[3])
                print(*IPinicial, sep =".")
            elif result[3] == 0 and result[2] > 0:
                IPinicial[2] = int(IPinicial[2]) + (int(255) - int(result[2]))
                print(*IPinicial, sep =".")

        elif IPinicial[3] <= 254:                
            print(" - ", end="")  
            print(*IPinicial, sep =".")
        print(f"El broadcast de la red es: ", end="")
        IPinicial[3] = int(IPinicial[3]) + int(1)
        print(*IPinicial, sep =".")
        if c==0:
            c = int(c) + int(1)
        print('\n')

datosp()

