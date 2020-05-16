# ProjetReseauxPython

## Explication du projet

Programme en Python qui offre la possibilité de dialoguer avec le programme https://github.com/CryTime/ProjetReseaux écrit en Ruby.

Ce chat permet au client, après qu'il se soit connecté, de pouvoir envoyer des messages publics à destinations de tout les
clients connectés au serveur.

Le client peut aussi envoyer des messages privés aux autres clients qui ne seront pas visibles aux clients non concernés.
Chaque client peut connaître la liste des clients connectés au chat. Pour se connecter au serveur le client doit écrire la commande "/pseudo", puis il lui sera demandé d’écrire le pseudonyme qu’il souhaitera utiliser dans le chat.
Une fois connecté pour pouvoir envoyer un message public, le client n'a juste qu’à écrire sur le terminal le texte qu’il veut envoyer et taper sur entrée pour l’envoyer à tout les autres clients.

Pour faire un message privé, il suffit d’écrire "msg", puis après un espace, le nom du pseudo
à qui on veut envoyer le message et après un autre espace pour délimiter, le texte que l’on veut envoyer au
client du chat voulu. Pour demander la liste de tous les clients connectés, il faut écrire "/list". Pour quitter le
chat, le client doit écrire "/quit" et il est automatiquement déconnecté du chat.


Schématisation du projet : C correspond au client, S correspond au serveur
-Connexion au serveur du chat : S -> C : "Bienvenue dans le Chat tapez pseudo si vous voulez vous connecter"
C -> S : "/pseudo" S -> C : "tapez le pseudo que vous voulez utiliser pour le chat :" C -> S : "Pseudo" S ->
C : "Bienvenue Pseudo"
-Liste des clients C -> S : "/list" S -> C : "Les personnes connectées sont : -pseudo1, -pseudo2 etc."
-Messages publics : C -> S : "texte" S -> Cx(les autres clients) : "texte"
-Messages privées : C1 -> S : "msg pseudoDeC2 texte" S -> C2 : "C1 vous a envoyer un message privé :
texte"
Déconnexion : C -> S : "/quit" S déconnecte C.
Ping : S -> C : "ping" C -> S : "pong" si il n’y a pas de réponse "pong" du client au "ping" du serveur, au
bout de X fois, il y a déconnexion du client qui ne répond pas.
Restrictions : Le pseudo ne peut être composé que de ces caractères(lettres de l’alphabet, chiffres, tiret du
bas, trait d’union) et ne doit comporter qu’entre 2 et 12 caractères.

## Lancer le programme
Pour lancer le programme, faire:
<pre><code>python3 projet.py</code></pre>

Après ça, vous devez choisir si vous voulez être côté Client ou côté Serveur:

![Optional Text](../master/images-readme/image_projet1.png)

Une fois fait, vous pouvez connecter plusieurs clients sur le même serveur et faire une discussion publique ou des messages privés.

