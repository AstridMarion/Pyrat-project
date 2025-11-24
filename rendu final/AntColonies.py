"""
    This file contains useful elements to define a particular player.
    In order to use this player, you need to instanciate it and add it to a game.
    Please refer to example games to see how to do it properly.
"""

# External imports
from typing import *
from typing_extensions import *
from numbers import *
from random import random,randrange,uniform
from Dijkstra import Dijkstra

# PyRat imports
from pyrat import Player, Maze, GameState, Action,Graph

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class AntColonies (Player):

    """
        This player is basically a player that does nothing except printing the phase of the game.
        It is meant to be used as a template to create new players.
        Methods "preprocessing" and "postprocessing" are optional.
        Method "turn" is mandatory.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:     Self,alpha=50,beta=50,
                   *args:    Any,
                   **kwargs: Any
                 ) ->        Self:

        """
            This function is the constructor of the class.
            When an object is instantiated, this method is called to initialize the object.
            This is where you should define the attributes of the object and set their initial values.
            Arguments *args and **kwargs are used to pass arguments to the parent constructor.
            This is useful not to declare again all the parent's attributes in the child class.
            In:
                * self:   Reference to the current object.
                * args:   Arguments to pass to the parent constructor.
                * kwargs: Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)

        # Print phase of the game
        print("Constructor")
        self.actions=[]
        self.alpha=alpha
        self.beta=beta
    

    def maze_to_graph(self:Self, graph:Graph,game_state:GameState)->Tuple[Graph,Dict[Integral,Dict[Integral,List[Integral]]]] :
        """
            crer un graph avec que les fromages et la position du joueur
        out:
            (graph_finale,graph_retour): graph_finale est le dit graphe
                                    graph_retour est l'équivanet d'un graph et permet de passer du graph_finale au graph initiale
        """
        source:Integral=game_state.player_locations[self.name]
        cheeses:List[Integral]=game_state.cheese
        graph_finale:Graph=Graph()
        graph_retour:Dict[Integral,Dict[Integral,List[Integral]]]={source:{}}
        graph_finale.add_vertex(source)
        for cheese in cheeses :
            graph_finale.add_vertex(cheese)
        player=Dijkstra()
        distance,routing_table=player.traversal(graph,source)
        for cheese in cheeses:
            graph_finale.add_edge(source,cheese,distance[cheese],symmetric=True)
            graph_retour[source][cheese]=player.find_route(routing_table,source,cheese)
        for cheese_int in cheeses :
            distance,routing_table=player.traversal(graph,cheese_int)
            graph_retour[cheese_int]={source:player.find_route(routing_table,cheese_int,source)}
            for cheese_fin in cheeses:
                if cheese_fin!=cheese_int:
                    #if not graph_finale.has_edge(cheese_fin,cheese_int):
                    graph_finale.add_edge(cheese_int,cheese_fin,distance[cheese_fin])
                    graph_retour[cheese_int][cheese_fin]=player.find_route(routing_table,cheese_int,cheese_fin)
        return (graph_finale,graph_retour)
    
    def route_mouse(self:Self,l:List[Integral],graph_retour:Dict[Integral,Dict[Integral,List[Integral]]])->List[Integral]:
        """
            Permet de passer du chemin dans le graphe avec que le frommage au chemin dans le maze initiale
        """
        reponse:List[Integral]=[l[0]]
        for i in range(len(l)-1):
            reponse.pop()
            reponse+=graph_retour[l[i]][l[i+1]]
            
        return reponse


    def AntColonies(self:Self,graph:Graph,source:Integral)->List[Integral]:
        #print(graph.vertices)

        def somme(tab):
            S=0
            for i in range(len(tab)):
                S+=tab[i][0]
            return S

        def choix_pondere(poids):
            """
                a améliorer
            """
            indice=uniform(0,somme(poids) )
            i=0
            while indice>poids[i][0]:
                indice-=poids[i][0]
                i+=1
            return poids[i][1]

        def longeur(chemin):
            poid=0
            for i in range(len(chemin)-1):
                poid+=graph.get_weight(chemin[i],chemin[i+1])
            return poid

        def depose_pheromones(pheromones, circuit):
            totale=longeur(circuit)
            for i in range(len(circuit)-1):
                pheromones[circuit[i]][circuit[i+1]]+=graph.get_weight(circuit[i],circuit[i+1])/totale
            return None
            
        def evapore_pheromones(pheromones, evaporation):
            for i in pheromones:
                for j in pheromones:
                    pheromones[i][j]*=evaporation
            return None
            
        def fourmi( pheromones, alpha, beta,source):
            circuit=[source]
            #print(pheromones)
            ville_non={source:"fait"}
            for _ in range (len(graph.vertices)):
                poid=[]

                for j in graph.vertices:
                    if not j in ville_non:
                        #print(circuit)
                        poid.append((pheromones[circuit[-1]][j]**alpha/((graph.get_weight(circuit[-1],j)**beta)),j))
                    else : poid.append((0,j))
                ville=choix_pondere(poid)
                ville_non[ville]="fait"
                circuit.append(ville)
            return circuit


        def aco( evaporation, alpha, beta, p,source):
            pheromones={}
            #print(graph.vertices)
            for i in graph.vertices:
                pheromones[i]={}
                for j in graph.vertices:
                    pheromones[i][j]=0.1
            for _ in range(p):
                circuit=fourmi( pheromones, alpha, beta,source)
                depose_pheromones( pheromones, circuit)
                evapore_pheromones(pheromones, evaporation)
            return glouton_max(pheromones,source)
            
        def glouton_max(distance,source):
            chemin=[source]
            ville_non={source:"fait"}
            while len(chemin) < len(graph.vertices):
                le_max=float("-inf")
                for i in graph.vertices:
                    if i!= chemin[-1]:
                        if not i in ville_non and distance [i][chemin[-1]]>le_max:
                            le_max=distance [i][chemin[-1]]
                            ville=i
                ville_non[ville]="fait" 
                chemin.append(ville)
            return chemin
        route=aco(0.1, self.alpha, self.beta, 100,source)
        return route


    

    




    

       
    #############################################################################################################################################
    #                                                               PYRAT METHODS                                                               #
    #############################################################################################################################################

    @override
    def preprocessing ( self:       Self,
                        maze:       Maze,
                        game_state: GameState,
                      ) ->          None:
        
        """
            This method redefines the method of the parent class.
            It is called once at the beginning of the game.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * None.
        """
        
        # Print phase of the game
        print("Preprocessing")
        graph,graph_retour=self.maze_to_graph(maze,game_state)
        route=self.route_mouse(self.AntColonies(graph,game_state.player_locations[self.name]),graph_retour)
        self.actions=maze.locations_to_actions(route)




    #############################################################################################################################################

    @override
    def turn ( self:       Self,
               maze:       Maze,
               game_state: GameState,
             ) ->          Action:

        """
            This method redefines the abstract method of the parent class.
            It is called at each turn of the game.
            It returns an action to perform among the possible actions, defined in the Action enumeration.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * action: One of the possible actions.
        """

        # Print phase of the game
        print("Turn", game_state.turn)

        # Return an action
        return self.actions.pop(0)

#############################################################################################################################################

    @override
    def postprocessing ( self:       Self,
                         maze:       Maze,
                         game_state: GameState,
                         stats:      Dict[str, Any],
                       ) ->          None:

        """
            This method redefines the method of the parent class.
            It is called once at the end of the game.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
                * stats:      Statistics about the game.
            Out:
                * None.
        """

        # Print phase of the game
        print("Postprocessing")
