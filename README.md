# PietInterpretor: Compilation de programmes en langage Piet
Interpréteur de langage Piet, avec un "launge" pouvant contenir plusieurs programmes à la fois.

Indications:
Pour chaque programme, deux petites led sont à disposition. Elles
servent à "partager" le stack et l'output du programme auquel elles
sont affiliées.

Exemple:
Prennons 3 programmes. Le premier "partage" son stack (LED du haut)
et son output (LED du bas). Alors le 2eme programme héritera
du stack et de l'output à la suite du premier programme.
Si le 2eme programme ne partage que son output, alors le 3eme
programme aura pour output d'entrée celui du programme 2, et pour stack
en entrée celui du 1er programme.


Prochain(e)s mises à jour / Patchs envisagé(e)s:
- Refactor du code (amélioration de la structure des classes,
  remplacement du français par l'anglais, variables privées...)
- Ajout de nouvelles couleurs qui seraient des programmes pré-codés
- Arrêt complet du launch de programmes sur appuie du bouton "Stop"
- Possibilité de faire des boucles conditionnelles dans le launge / 
  des branchements entre programmes
- Adapter la taille des textes & remplacer tous les boutons tkinter
  par des boutons à taille adaptative à la taille de l'écran
- Duplication de programmes dans le launge
- Laboratoire de couleurs

Dernières mises à jour (historique simplifié):\
Version 1.0 => Interpréteur textuel de Piet\
Version 1.1 => Corrections de bugs et déployements sur git\
Version 2.0 => Interface graphique, première version\
Version 3.0 => Correction totale de l'interface graphique, customisation
               de certaines commandes Piet, ajout d'un input en attente passive\
Version 3.1 => Début de création du launge, stack de programme,
	       enregistrement des Stacks et Outputs\
Version 4.0 => Launge fonctionnel, lancement des programmes, corrections
	       sur le partage des Stacks et Outputs\
Version 4.1 => Lancement graphique et non plus textuel des programmes
               depuis le Launge
Version 5.0 => Mise à jour des Sets: ajout de la possibilité de
	       customiser les Sets de couleurs utilisés sur l'interface
               graphique\
Version 5.1 => Corrections sur la mise à jour des Sets, et vérification
               avant lecture d'un programme que les couleurs présentes
               dans le programme correspondent aux couleurs des Sets\
Version 5.2 => Correction de la mise à jour des Sets:\
	* Changement du format de fichier pour les programmes => On peut accueillir plus de couleurs. Les sets sont exportés & importés\ 
	* A l'import d'un programme, les sets de base et le choix des sets est correctement modifié\
Version 5.3 => Mise à jour des Sets complétée (pour le moment)\
	* Les sets sont enregistrés avec les programmes dans le launge\
	=> On peut donc lancer une succession de programmes
	   avec des sets différents\
Version 5.4 => Mise à jour et patch du lancement de la compilation de programmes\
	* Les fonctions lastSharedStack et lastSharedOutput fonctionnent sans anomalie\
	* Le lancement des programmes ne génère qu'une seule fenêtre dont la zone de code change\
		-> + beau et + clair\
		-> La succession des programme se déroule sans anomalie\
