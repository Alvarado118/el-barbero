import threading 
import time

sillas = threading.Semaphore(4)

barberoListo = threading.Semaphore(1)

clienteListo = threading.Semaphore(1)
corteTerminado = threading.Semaphore(1)


sillasDisponibles = 4

TotalClientes = 0

def corteFinalizado():
    print('\nCorte finalizado\n')
    corteTerminado.release()


def cortarCabello():
    print('Cortando el pelo encontro un piojo xD...')
    time.sleep(3)
    corteFinalizado()


def funcionBarbero():

    #el barbero trabajara siempre cuando un cliente llegua

    global TotalClientes

    while TotalClientes == 0:
        print('No hay clientes. El barbero duerme un rato zzz...')
        #time.sleep(2)
    while TotalClientes > 0:
        #Esperara un cliente cuando llegue
        clienteListo.acquire()
        global sillasDisponibles 
        print('\nEl barbero atiende al cliente')
        #número de sillas disponibles incremente
        sillasDisponibles += 1
        sillas.release()
        print('Sillas disponibles: ', sillasDisponibles)
        print('nuemero de clientes (sumando al que está siendo atendido): ', TotalClientes)
        #Y ahora sí comenzra a cortar el cabello
        cortarCabello()
        #terminó de cortar el cabello, está listo para ir con el siguiente 
        barberoListo.release()
        TotalClientes -= 1
    

def funcionCliente(index):
    #llega al negocio y obsrva si hay sillas disponibles
    print('\nLlega cliente: ', index)
    global sillasDisponibles
    if(sillasDisponibles>0):
        #agarra una silla
        sillas.acquire()
        sillasDisponibles -= 1
        global TotalClientes
        TotalClientes += 1
        print('El cliente se sienta en una silla')
        print('El cliente indica que está listo para recibir el corte')
        print('Sillas disponibles: ', sillasDisponibles)
        print('Total de clientes (sumando al que está siendo atendido): ', TotalClientes)
        clienteListo.release()
        #esperara a que el barbero termine de cortarle el cabello al cliente que esta
        corteTerminado.acquire()
        barberoListo.acquire()
        #por fin es su turno 
    
    #ya noy hay sillas y mejor se retira del lugar
    else:
        print('\nEl cliente se retira del lugar por que ya no hay espacio en el negosio ni sillas xD')

def main():
    #band = True
    while True:
        print("Cuando el programa finalice, por favor indica si quieres repetir el procedimiento o si no, no. (s/n)")
        barbero = threading.Thread(target=funcionBarbero)
        num = int(input("ponga el numero de clientes que deben ser antendidos: "))
        
        barbero.start()
        listaClientes = list()
        for index in range(num):
            c = threading.Thread(target=funcionCliente, args=(index+1,))
            listaClientes.append(c)
            time.sleep(1)
            c.start()
        time.sleep(3*num)
        value = input('¿Deseas repetir el prtocedimiento? s/n.\n')
        if(value == "n" or value == "N"):
            break

if __name__ == '__main__':
   main()
