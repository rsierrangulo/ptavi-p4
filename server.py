#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time

comandos = sys.argv

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    
    diccionario = {}
    lista_usuario = []
 

    def register2file(self):
        self.fichero = open('registered.txt', 'w')
        self.fichero.write("User" + '\t\t\t\t' + "IP" + '\t\t\t' + "Expires" + '\r\n')
        for usuario in self.diccionario:
            self.fichero.write(usuario + '\t' + self.diccionario[usuario][0] + '\t' + self.diccionario[usuario][1] + '\r\n') 
        self.fichero.close()
        

    def handle(self):
        while 1:
            line = self.rfile.read()
            print "Peticion del cliente: " + line
            lista = line.split(" ")
            if lista[0] == "REGISTER":
                #tiempo = time.time() + float(lista[5])
                #tiempo_actual = time.time()
                hora = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(float(time.time()) + float(lista[5])))
                hora_actual = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(float(time.time())))
            #    if tiempo actual < tiempo:
                    
                self.lista_usuario = [self.client_address[0], hora]
                self.diccionario[lista[2]] = self.lista_usuario
                self.wfile.write(lista[3] + " 200 OK" + "\r\n\r\n")
                print "Diccionario al añadir usuarios:"
                print self.diccionario
                if int(lista[5]) == 0:
                    del self.diccionario[lista[2]]
                    self.wfile.write(lista[3] + " 200 OK" + "\r\n\r\n")
                    print "Diccionario al borrar usuarios:"
                    print self.diccionario
                print lista[3] + " 200 OK" + "\r\n\r\n"
            else:
                print "Petición inválida"
            self.register2file()
            if not line:
                break


if __name__ == "__main__":
    serv = SocketServer.UDPServer(("", int(comandos[1])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
