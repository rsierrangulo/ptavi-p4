#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de registro SIP
"""

import SocketServer
import sys
import time


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """Register SIP"""

    clientes = {}

    def register2file(self):
        """Escribe en el fichero el diccionario"""
        fichero = "registered.txt"
        fichero = open(fichero, "w")
        cadena = "User\tIP\tExpires\r\n"

        for cliente in self.clientes.keys():
            #Ponemos la hora en el formato deseado
            hora = time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.gmtime(self.clientes[cliente][1]))
            cadena += (cliente + "\t" + self.clientes[cliente][0] +
                       "\t" + hora + "\r\n")
        #Escribimos el diccionario en el fichero
        fichero.write(cadena)

    def handle(self):
        """ Registra y borra clientes del server"""
        self.wfile.write("Hemos recibido tu peticion")
        while 1:
            # Leemos las lineas del fichero
            line = self.rfile.read()
            if not line:
                break
            palabras = line.split()
            direccionsip = palabras[1]
            direccion = direccionsip.split(":")
            expires = palabras[4]
            horalim = time.time() + float(expires)
            # Añadimos una entrada al diccionario
            self.clientes[direccion[1]] = (self.client_address[0], horalim)
            vsip = palabras[2]
            print vsip + " 200 OK \r\n\r\n"
            # Borramos si expires = 0 o el registro ha caducado
            if expires == "0":
                del self.clientes[(direccion[1])]
            for cliente in self.clientes.keys():
                if self.clientes[cliente][1] < time.time():
                    del self.clientes[cliente]
            self.register2file()

if __name__ == "__main__":
    """ Creamos servidor SIP y escuchamos"""
    puerto = int(sys.argv[1])
    serv = SocketServer.UDPServer(("", puerto), SIPRegisterHandler)
    print "Lanzando servidor register..."
    serv.serve_forever()
