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
        """
        Método que imprime en el fichero el contenido del diccionario
        """
        fichero = open('registered.txt', 'w')
        fichero.write("User" + '\t\t\t' + "IP" + '\t\t\t' + "Expires" + '\r\n')
        for usuario in self.diccionario.keys():
            # El user se imprime como "sip:usuario" debido a que se guarda así
            # en la lista
            fichero.write(usuario + '\t' + self.diccionario[usuario][0] + '\t')
            hora = time.gmtime(self.diccionario[usuario][1])
            fichero.write(time.strftime('%Y-%m-%d %H:%M:%S', hora) + '\r\n')
        fichero.close()

    def handle(self):
        """
        Método handle
        """
        while 1:
            line = self.rfile.read()
            print "Peticion del cliente: " + line
            lista = line.split(" ")
            print lista
            if lista[0] == "REGISTER":
                tiempo = time.time() + float(lista[3])
                tiempo_actual = time.time()
                self.lista_usuario = [self.client_address[0], tiempo]
                self.diccionario[lista[1]] = self.lista_usuario
                for usuario in self.diccionario.keys():
                    if self.diccionario[usuario][1] < tiempo_actual:
                        del self.diccionario[usuario]
                    self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                print "SIP/2.0 200 OK\r\n\r\n"
            else:
                print "SIP/2.0 400 Bad Request\r\n\r\n"
                self.wfile.write("SIP/2.0 400 Bad Request\r\n\r\n")
            self.register2file()
            if not line:
                break


if __name__ == "__main__":
    """
    Procedimiento principal
    """
    serv = SocketServer.UDPServer(("", int(comandos[1])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
