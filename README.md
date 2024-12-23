# PietInterpretor
Interpréteur de langage Piet, avec un "launge" pouvant contenir plusieurs programmes à la fois

Si vous cliquez sur "Lancer", c'est la console python qui affichera
le résultat final (stack + output) pour le moment.

Indications:
Pour chaque programme, deux petites led sont à disposition. Elles
servent à "partager" le stack et l'output du programme auquel elles
sont affiliées.

Exemple:
Prennons 3 programmes. Le premeier "partage" son stack (LED du haut)
et son output (LED du bas). Alors le 2eme programme héritera
du stack et de l'output à la suite du premier programme.
Si le 2eme programme ne partage que son output, alors le 3eme
programme aura pour output d'entrée celui du programme 2, et pour stack
en entrée celui du 1er programme.


Prochain(e)s mises à jour / Patchs envisagé(e)s:
- Faire des thèmes de couleur pour l'Interpréteur Graphique
- Refactor du code (amélioration de la structure des classes,
  remplacement du français par l'anglais, variables privées...)
- Ajout de nouvelles couleurs qui seraient des programmes pré-codés
- Arrêt complet du launch de programmes sur appuie du bouton "Stop"
- Possibilité de faire des boucles conditionnelles dans le launge / 
  des branchements entre programmes
- Adapter la taille des textes & remplacer tous les boutons tkinter
  par des boutons à taille adaptative à la taille de l'écran
