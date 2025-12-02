# Auteurs

Forian THOLLOT
Astrid MARION
Léna ROUZIERES

# Objectifs
<div style="overflow: auto; margin-bottom: 20px;">
<img alt="image" src="https://github.com/user-attachments/assets/882cc204-b8b6-497d-ab69-db61cf9c5499" style="float: left; width: 187px; height: 270px; margin-right: 15px;">
Le projet a été réalisé dans le cadre de la formation FISE A1 à IMT Atlantique, et est centré sur un logiciel appelé PyRat. En quelques mots, ce logiciel est un jeu vidéo, dans lequel un petit rat est contrôlé dans un labyrinthe grâce à des codes Python. Il y a des morceaux de fromage à différents endroits du labyrinthe, que le rat veut manger. Dans un premier temps, l'objectif a été d’aider le rat à manger tous les morceaux de fromage. Ensuite, nous avons introduit un ou plusieurs autres joueurs, qui doivent également ramasser des fromages. L’objectif est alors de ramasser plus de morceaux de fromage que ceux-ci.
</div>

<table>
  <tr>
    <td style="width: 187px; padding-right: 15px; vertical-align: top; border: none;">
      <img alt="image du rat PyRat" src="https://github.com/user-attachments/assets/882cc204-b8b6-497d-ab69-db61cf9c5499" width="187" height="270">
    </td>
    <td style="vertical-align: top; border: none;">
      Le projet a été réalisé dans le cadre de la formation FISE A1 à IMT Atlantique, et est centré sur un logiciel appelé PyRat. En quelques mots, ce logiciel est un jeu vidéo, dans lequel un petit rat est contrôlé dans un labyrinthe grâce à des codes Python. Il y a des morceaux de fromage à différents endroits du labyrinthe, que le rat veut manger. Dans un premier temps, l'objectif a été d’aider le rat à manger tous les morceaux de fromage. Ensuite, nous avons introduit un ou plusieurs autres joueurs, qui doivent également ramasser des fromages. L’objectif est alors de ramasser plus de morceaux de fromage que ceux-ci.
    </td>
  </tr>
</table>

# Notions abordées:

* Théorie des graphes
* Algorithmes classiques
* Résolution de problèmes de complexité croissante


# Joueurs

**1. Exhaustive:**  
Trois fonctions permettent de trouver le chemin complet optimisé pour visiter tous les fromages:
* maze_to_graph:
    - permet de créer un graph reliant chaque tous les sommets (position initiale ou fromage) entre eux. Les arrêtes de ce graphe sont pondérées par la distance minimale les reliant (trouvée avec Dijkstra). Cette fonction permet aussi de garder en mémoire les chemins trouvés entre chaque sommets grâce à Dijkstra.
    - sa complexité est en O(n_sommets**2*log(n_sommets)) car les opérations les plus coûteuses sont les recherches Dijkstra
* TSP :
    - permet de trouver l ordre des sommets à visiter qui optimise le temps de parcours. C est une solution de force brute
    - sa complexité est en O(nb_sommet*(nb_sommets−1)!) ce qui risque d être trop important si le nombre de fromages est trop élevé
* route_mouse:
    - permet de donner le chemin exact à suivre par la souris pour visiter les fromages dans l ordre qu a donné le TSP et grâce aux chemins reliant chaque sommets mémorisés avec maze_to_graphe.
    - sa complexité est en O(nb_sommets)

**2. Backtracking:**  
Cette fonction est une amélioration de la fonction précédente Exhaustive.
En effet, la seule fonction modifiée est TSP qui devient Backtracking. Cette fonction possède les 
caractériqtiques suivantes:
- c est une fonction récursive
- Elle a la même typologie que Exhaustive mais à chauque fois qu'on évalue un chemin, on s'arrête s'il 
est plus long qu'une solution précédente. 
- Cette solution est donc plus optimisée dans le meilleure des cas que Exhaustive et renvoie exactement la même solution
- sa complexité est en O(nb_sommet*(nb_sommets−1)!) dans le pire des cas (comme Exhaustive)

**3. SortedNeighbors:**  
C est encore une amélioration de la fonction Backtracking.
En effet, la seule fonction modifiée est Backtracking qui devient SortedNeighbors. Cette fonction possède les caractériqtiques suivantes:
- c est une fonction récursive
- elle possède la même typologie que Backtracking et renvoie exactement la même solution. Cependant maintenant, les sommets sont visités par ordre croissant du poids de l'arrête le reliant au sommet précédent. Cela permet d'éliminer plus rapidement des chemins trop longs.
- sa complexité est en O(nb_sommet*(nb_sommets−1)!) dans le pire des cas (comme Exhaustive)

**4. Greedy:**  
C'est un joueur utilisant une nouvelle méthode de recherche:
La seule fonction modifiée par rapport à Exhaustive est toujours le TSP qui devient greedy. 
Cette fonction possède les caractériqtiques suivantes:
- c est une fonction itérative
- elle possède la même typologie que Exhaustive
- elle utilise l'heuristique suivante: 
"le chemin le plus court qui passe par tous les morceaux de fromage peut être approximé en allant séquentiellement vers le morceau de fromage le plus proche"
- sa complexité est en O(nb_sommets**2)

**5. GreedyEachTurn:**  
(Nous n'avons pas fait GreedyEachCheese étant donné que GreedyEachTurn est déjà une amélioration 
de celui-ci)
C'est une amélioration de Greedy qui calcul à chaque tour le chemin à parcourir afin de pouvoir 
jouer contre un adversaire.
Ainsi, si le fromage visé est attrapé par un adversaire avant de l'atteindre, la souris n'ira plus le chercher.
Ce joueur n'utilise que des méthodes  Pyrat:
* __init__:
    introduit une nouvelle variable cheese à laquelle est associée la position du fromage visé afin 
    de vérifier 
    qu'il n'a pas déjà été mangé
* preprocessing:
    - recherche seulement le premier fromage le plus proche à aller attraper
    - sa complexité est en O(nb_fromages)
* turn:
    - si le fromage est toujours présent, il continue son chemin vers celui-ci
    - sinon, il cherche à nouveau le fromage le plus proche toujours présent
    - sa complexité est au pire en O(nb_fromages)

Pour tous les nouveaux jeux créés à partir de visualize_Exhaustive jusqu'à visualiza_GreedyEachTurn, 
plusieurs fromages sont mis en paramètres afin d améliorer le jeux, et la boue a été laissée car le 
problème de la boue a déjà été traité précédemment.
Dans la CONFIG, le paramètre game_mode permet en cas d erreur d avoir une description détaillée du 
problème afin de facilité la résolution.
Les jeux pour Exhaustive, Backtracking, SortedNeighbors et Greedy ont la même structure de base.
Cependant, le jeux pour GreedyEachTurn inove en introduisant deux joueurs sur le même plateau de jeu. 
Cela permet d observer le comportement d une souris si un adversaire attrape le fromage qu elle visait 
avant elle.>

# Tests unitaires

Chaque test verifie si les fonctions revoie les bons types en sortie.
Et voilà les tests réalisés pour chaque fonction (apparaissant dans plusieurs joueurs)
* maze_to_graph: 
    - tous les fromages et la localisation des joueurs sont bien c=retranscrits dans le graph
    - on aurait pu vérifier que le chemin renvoyé est bien optimisé mais nous n'avons pas eu le temps
* route_mouse:
    - vérifie que le chemin trouvé possède bien des cases adjacentes
* TSP:
    - vérifie que le chemin passe bien par tous les sommets
* Backtracking:
    - vérifie qu'il s'arrête dès qu'une longueur plus longue est trouvée
* SortedNeighbors:
    - le trie est effectué avant de visiter les sommets
    - il faut avoir visité tous les sommets
    - les premgit piers sommets visités sont ceux à une distance minimale
