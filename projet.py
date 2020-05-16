# -*- coding: utf-8 -*- 

import os
import sys
import socket
import select
import threading
import signal
import errno
from itertools import groupby
from select import select
import subprocess #pour lire dans stdout
#import datetime
from datetime import datetime, timedelta
import csv
import os.path
from datetime import datetime as dt
from subprocess import Popen, PIPE
import fcntl

HOST = str()
PORT = int()
liste_client = {}
liste_client_thread = {}
VAR_TEMOIN_BREAK = 0
VARTOTO = 0

def fonctionPrincipale () :
    global HOST
    global PORT
    val = 2
    while(1):
        choix = input('Pour être du côté client, écrire: "Client"\n Pour être du côté serveur, écrire: "Serveur"\n Que choisissez-vous?\n:')
        if choix == 'Serveur':
            print ('Vous avez choisi', choix)
            portserveur = input('Quel port choisissez-vous?\n:')
            portserveur_int = int(portserveur)
            PORT = portserveur_int
            val = 0
            if os.path.isfile("fichier_liste_client.csv") == True:
                os.system("rm fichier_liste_client.csv")
            os.system("touch fichier_liste_client.csv")   
            return val

        if choix == 'Client':
            print ('Vous avez choisi', choix)
            hoteclient = input('Quel hôte choisissez-vous?\n:')
            "Vous avez choisi l'hôte '{}'".format(hoteclient)
            portclient = input('Quel port choisissez-vous?\n:')
            portclient_int = int(portclient)
            'Vous avez choisi le port {}'.format(portclient_int)
            HOST = hoteclient
            PORT = portclient_int
            val = 1
            return val

        if choix != 'Serveur' and choix !='Client':
            print("ce choix n'existe pas veuillez recommencez\n")
    return val


def compte_mot(phrase):
    mots = phrase.split(' ')
    return len(mots)

def compte_caracteres(mot):
    nb_caracteres = 0
    for i in mot:
        nb_caracteres += 1
    return nb_caracteres

def verif_validite_du_pseudo(pseudo):
    for i in pseudo:
        if i != chr(45) and i != chr(95) and (not (i >= chr(48) and i <= chr(57))) and (not(i >= chr(65) and i <= chr(90))) and (not(i >= chr(97) and i <= chr(122))):
            return False
    return True

def initFichier(dictionnaire):
    with open('fichier_liste_client.csv', 'wb') as csv_file:
        for key in dictionnaire:
            csv_file.write(key.encode() + '\n'.encode())

def recupereListe():
    fichier = open("fichier_liste_client.csv", "r")
    mon_texte = fichier.read()
    fichier.close()
    ma_liste = []
    mon_texte_divise = mon_texte.split('\n')
    for i in range(0, len(mon_texte_divise)-1):
        ma_liste.append(mon_texte_divise[i])
    return ma_liste

class ThreadReception(threading.Thread):
    """objet thread gérant la réception des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
        
    def run(self):
        while 1:
            message_recu = self.connexion.recv(1024)
            if message_recu.decode().strip() == "Déconnexion".strip() or message_recu.decode().strip() == "Deconnexion".strip():
                print("dans déco2")
                break
            if message_recu.decode().strip() == "ping".strip():
                self.connexion.send("pong\n".encode());
                continue
            
            else:
                if message_recu.decode() != 'Ce pseudo existe déjà\nDéconnexion\n' or message_recu.decode().strip() != "\n\n".strip():
                    print ((message_recu.decode()))
                else:
                    print("dans déco3")
                    break

        print ("Client arrêté. Connexion interrompue.")
        self.connexion.close()
        os._exit(0)

class ThreadEmission(threading.Thread):
    """objet thread gérant l'émission des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
        
    def run(self):
        global VAR_TEMOIN_BREAK
        global liste_client

        while 1:
            message_emis = str()

            ma_liste_client = recupereListe()

            message_emis = input()
            self.connexion.send((message_emis+"\n").encode())
            #print("message_emis=" + message_emis + "fin")
            if message_emis == '/quit':
                break
            if message_emis == "/pseudo":
                VAR_TEMOIN_BREAK = 1

            """            
            if message_emis in ma_liste_client and VAR_TEMOIN_BREAK == 1:
                print("Ce pseudo existe déjà\nDéconnexion\n")
                VAR_TEMOIN_BREAK = 0
                message_emis = "/quit"
            """

            if message_emis in ma_liste_client and VAR_TEMOIN_BREAK == 0:
                VAR_TEMOIN_BREAK = 0
            

            if message_emis == "/quit":
                break
            
class ThreadClient(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
        self.connecte = False
        
    def run(self):
        global liste_client
        global liste_client_thread 
        nom = self.getName() 
        nom2base = self.getName()
        message = str()
        ancien_nom = nom.encode()
        compteur2changements2pseudos = -1
        possibilite2connexion = 1
        messageL = str()
        nom_du_destinataire = str()
        messageMP = str()
        messageP = str()
        messageM = str()
        pseudo = str()
        pseudo_deja_utilise = 0

        
        period = timedelta(seconds=1)
        next_time = datetime.now() + period
        minutes = 0
        
        while 1: 
            """           
            if next_time <= (datetime.now()+timedelta(seconds=5)) and self.connecte == True:
                    print("dans CHANGEMENT msgCLIENT")
                    msgClient = "ping\n"
            """
            """
                    minutes += 1
                    next_time += period

                    maintenantPong = datetime.now()
                    heure_precisePong = str(maintenantPong.hour) + '.' + str(maintenantPong.minute) + '.' + str(maintenantPong.second)
                    print("[" + heure_precisePong + "]:" + "pong de " + pseudo)
            """
            

            """
                    for cle in conn_client:
                        if cle == nom2base:
                            conn_client[cle].send("ping".encode())
            """
            
            
            try:
                msgClient = self.connexion.recv(1024)
            except socket.error as e:
                if e.errno != errno.ECONNRESET:
                    raise 
                pass
            print(msgClient.decode())

            if msgClient.decode() == "ping\n" and self.connecte == True:
                maintenantPong = datetime.now()
                heure_precisePong = str(maintenantPong.hour) + '.' + str(maintenantPong.minute) + '.' + str(maintenantPong.second)
                print("[" + heure_precisePong + "]:" + "pong de " + pseudo)
            if msgClient.decode().strip() == "/pseudo".strip():
                msg_emis_sans_pseudo = ''
                compteur1 = 0
                if compte_mot(msgClient.decode()) == 1:
                    for cle in conn_client:
                        if cle == nom2base:
                            conn_client[cle].send("Entrez votre pseudo\n".encode())
                            pseudo = self.connexion.recv(1024).decode()
                    if compte_caracteres(pseudo.strip()) < 2 or compte_caracteres(pseudo.strip()) > 12:

                        for cle in conn_client:
                            if cle == nom2base:
                                conn_client[cle].send("le pseudo proposé est invalide, car il ne correspond aux critères obligatoires d'un nom de pseudo définis par le protocole\n".encode())
                    else:
                        if verif_validite_du_pseudo(pseudo.strip()) == True:
                            if pseudo in liste_client :
                                pseudo_deja_utilise = 1
                                possibilite2connexion = 0
                                for cle in conn_client:
                                    if cle == nom2base:
                                        conn_client[cle].send("Ce pseudo existe déjà\nDéconnexion\n".encode())
                                if nom in liste_client:
                                    del liste_client[nom]
                                if nom in liste_client_thread:
                                    del liste_client_thread[nom]
                                break
                            if pseudo not in liste_client and pseudo_deja_utilise == 0:
                                self.connecte = True
                                possibilite2connexion = 1
                                compteur2changements2pseudos += 1
                                ancien_nom = nom
                                nom = str()
                                nom = pseudo
                                if ancien_nom in liste_client:
                                    del liste_client[ancien_nom]
                                if ancien_nom in liste_client_thread:
                                    del liste_client_thread[ancien_nom]
                                liste_client[nom] = nom
                                liste_client_thread[nom2base] = nom
                                messageP = "----------------------\nUtilisateurs en ligne:\n"
                                for cle in liste_client:
                                    messageP += '=> ' + cle + '\n'
                                messageP += "----------------------\n"
                        else:
                            for cle in conn_client:
                                if cle == nom2base:
                                    conn_client[cle].send("le pseudo proposé est invalide, car il ne correspond aux critères obligatoires d'un nom de pseudo définis par le protocole\n".encode())
                else:
                    for cle in conn_client:
                        if cle == nom2base:
                            conn_client[cle].send("le pseudo proposé est invalide, car il ne correspond aux critères obligatoires d'un nom de pseudo définis par le protocole\n".encode())
                
            if msgClient[0:3].decode() == 'msg' and self.connecte == True:
                compteur_i = 0
                msgClient_divise = msgClient.decode().split(' ')
                nom_du_destinataire = msgClient_divise[1]
                maintenantMP = datetime.now()
                heure_preciseMP = str(maintenantMP.hour) + '.' + str(maintenantMP.minute) + '.' + str(maintenantMP.second)
                messageMP = '[' + heure_precise + ']-' + "message privé de " + nom.strip() + ': '
                for i in msgClient.decode():
                    compteur_i += 1
                    if compteur_i > 5 + len(nom_du_destinataire):
                        messageMP += i

            if msgClient.decode().strip() == '/list' and self.connecte == True:
                messageL = "----------------------\nUtilisateurs en ligne:\n"
                for cle in liste_client:
                    messageL += '=> ' + cle + '\n'
                messageL += "----------------------\n"
            if msgClient.decode().strip() == "/quit":
                for cle in conn_client:
                        if cle == nom2base:
                            conn_client[cle].send("Deconnexion\n".encode())
                messageQ = "Deconnexion."
                if nom in liste_client:
                    del liste_client[nom]
                if nom in liste_client_thread:
                    del liste_client_thread[nom]
                break

            else:
                maintenant = dt.now()
                heure_precise = str(maintenant.hour) + '.' + str(maintenant.minute) + '.' + str(maintenant.second)
                messageM = '[' + heure_precise + ']-' + nom.strip() + ': ' + msgClient.decode()
            
            for cle in conn_client:
                if cle == nom2base and msgClient.decode().strip() == '/list':
                    message = messageL
                    conn_client[cle].send(message.encode())
                if cle == nom2base and msgClient.decode().strip() == '/pseudo':
                    message = messageP
                    conn_client[cle].send(message.encode())
                if cle == nom2base and msgClient.decode().strip() == '/quit':
                    message = messageQ
                    conn_client[cle].send(message.encode())
                if cle != nom2base and (msgClient.decode().strip() != '/list' and msgClient.decode().strip() != '/pseudo' and msgClient[0:3].decode().strip() != 'msg' and msgClient.decode().strip() != '/quit') and nom in liste_client and msgClient.decode() != 'ping\n':
                    message = messageM
                    conn_client[cle].send(message.encode())
                if cle in liste_client_thread:
                    if liste_client_thread[cle].strip() == nom_du_destinataire.strip() and msgClient[0:3].decode() == 'msg':
                        message = messageMP
                        conn_client[cle].send(message.encode())
                
                initFichier(liste_client)

        self.connexion.close()
        del conn_client[nom2base]
        print ("Client " + nom2base + "(pseudo:" + nom.strip() + ") s'est déconnecté." )
        for cle in conn_client:
            if cle != nom2base in liste_client_thread:
                maintenant_d = datetime.now()
                heure_precise_d = str(maintenant.hour) + '.' + str(maintenant.minute) + '.' + str(maintenant.second)
                messageDeconnexion =  '[' + heure_precise_d + ']-' + "Déconnection de " + nom
                conn_client[cle].send(messageDeconnexion.encode())


if __name__ == '__main__':
    f = fonctionPrincipale()
    if f == 0:
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            mySocket.bind((HOST, PORT))
        except socket.error:
            print ("La liaison du socket à l'adresse choisie a échoué.")
            sys.exit()
        print ("-------------------------------------\n-serveur prêt à recevoir des clients-\n-------------------------------------\n\nen attente de requêtes...\n")
        print(PORT)
        mySocket.listen(5)

        conn_client = {} 
        while 1:
            connexion, adresse = mySocket.accept()
            th = ThreadClient(connexion)
            th.start()
            it = th.getName()
            conn_client[it] = connexion
            print("---------\n-serveur-\n---------");
            connexion.send("bienvenue dans le chat, enregistrez-vous avec la commande /pseudo\n".encode())
    if f == 1:
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            connexion.connect((HOST, PORT))
        except socket.error:
            print ("La connexion a échoué.")
            sys.exit()
        print ("Connexion établie avec le serveur.")
        th_E = ThreadEmission(connexion)
        th_R = ThreadReception(connexion)
        th_E.start()
        th_R.start()

