#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys

comandos = sys.argv

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        self.diccionario = {}
        while 1:
            line = self.rfile.read()
            print "Peticion del cliente: " + line
            lista = line.split(" ")
            if lista[0] == "REGISTER":
                self.diccionario[lista[2]] = self.client_address[0]
                self.wfile.write(lista[3] + " 200 OK" + "\r\n\r\n")
                if int(lista[5]) == 0:
                    del self.diccionario[lista[2]]
                    self.wfile.write(lista[3] + " 200 OK" + "\r\n\r\n")
                print lista[3] + " 200 OK" + "\r\n\r\n"
            else:
                print "Petición inválida"
            if not line:
                break

if __name__ == "__main__":
    serv = SocketServer.UDPServer(("", int(comandos[1])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
