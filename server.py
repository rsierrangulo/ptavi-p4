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
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.diccionario = {}
        while 1:
            line = self.rfile.read()
            lista = line.split(" ")
            if lista[0] == "REGISTER":
                self.diccionario[lista[1]] = self.client_address[0]
                print "El cliente nos manda " + lista[1] + " 200 OK\r\n\r\n"
                self.wfile.write(lista[1] + "OK\r\n\r\n")
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", int(comandos[1])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
