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
import numpy as np

# PyRat imports
from pyrat import Player, Maze, GameState, Action,Graph

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class AntElit (Player):

    """
        This player is basically a player that does nothing except printing the phase of the game.
        It is meant to be used as a template to create new players.
        Methods "preprocessing" and "postprocessing" are optional.
        Method "turn" is mandatory.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:     Self,alpha=50,beta=50,ant=1500,p=0.1,
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
        self.ant_nb=ant
        self.p=p
    

    def maze_to_graph(self:Self, graph:Graph,game_state:GameState)->Tuple[Graph,Dict[Integral,Dict[Integral,List[Integral]]]] :
        """
            crer un graph avec que les fromages et la position du joueur
        out:
            (graph_finale,graph_retour): graph_finale est le dit graphe
                                    graph_retour est l'équivanet d'un graph et permet de passer du graph_finale au graph initiale
        """
        source:Integral=game_state.player_locations[self.name]
        cheeses:List[Integral]=game_state.cheese
        #print(cheeses)
        #print(source)
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


    def graph_normalisation(self:Self,graph:Graph)->Graph:
        """
            normalise le graph
        """
        max_weight:int=0
        for vertex1 in graph.vertices:
            for vertex2 in graph.vertices:
                if vertex1!=vertex2:
                    max_weight=max(max_weight,graph.get_weight(vertex1,vertex2))

        graph_norm:Graph=Graph()
        for vertex in graph.vertices:
            graph_norm.add_vertex(vertex)
        for vertex in graph.vertices:
            for vertex2 in graph.vertices:
                if vertex!=vertex2:
                    graph_norm.add_edge(vertex,vertex2,graph.get_weight(vertex,vertex2)/max_weight)
        return graph_norm
    


    def AntColonies(self:Self,graph:Graph,source:Integral)->List[Integral]:

        pheromones:dict[Integral,dict[Integral,int]]={}
        for i in graph.vertices:
            pheromones[i]={}
            for j in graph.vertices:
                pheromones[i][j]=0.1

        def choose_vertex(weights:List[Tuple[float,Integral]])->Integral:
            """
            c'est la fonction somme + choix pondéré
            """
            total:float=0
            for i in range(len(weights)):
                total+=weights[i][0]
            indice:float=uniform(0,total)
            i:int=0
            while indice>weights[i][0]:
                indice-=weights[i][0]
                i+=1
            return weights[i][1]

        def path_weight(chemin:List[Integral])->int:
            """
            c'est la fonction longueur
            """
            poid:int=0
            for i in range(len(chemin)-1):
                poid+=graph.get_weight(chemin[i],chemin[i+1])
            return poid
        

        def drop_pheromones(path:List[Integral]):            
            """
            In:
                *path : List[Integral] : path of the ant
            Out:
                None
            This function drops pheromones on the path of the ant
            """
            #print(circuit)
            totale:int=path_weight(path)
            for i in range(len(path)-1):
                pheromones[path[i]][path[i+1]]+=graph.get_weight(path[i],path[i+1])/totale
            return None
        
            
        def evapore_pheromones(evaporation:float):
            """
            In:
                *evaporation : float : evaporation rate
            Out:
                None
            This function evaporates pheromones
            """
            for i in pheromones:
                for j in pheromones:
                    pheromones[i][j]*=evaporation
            return None
        


            
        def ant(alpha:float, beta:float,source:Integral)->List[Integral]:
            """
            In:
                *alpha : float : coefficient of the importance of pheromones
                *beta : float : coefficient of the importance of weights
                *source : Integral : source vertex
            Out:
                *List[Integral] : path of the ant
            This function creates a path for an ant considering the pheromones and the weights
            """
            path:List[Integral]=[source]
            vertex_seen:dict[Integral,str]={source:"already seen"}
            for _ in range (len(graph.vertices)):
                weights:List[Tuple[float,Integral]]=[]

                for vertex in graph.vertices:
                    if not vertex in vertex_seen:
                        weight_vertex=pheromones[path[-1]][vertex]**alpha/((graph.get_weight(path[-1],vertex)**beta))
                        weights.append((weight_vertex,vertex))
                    else : weights.append((0,j))
                ville=choose_vertex(weights)
                vertex_seen[ville]="already seen"
                path.append(ville)
            return path
        

                    
        def glouton_max(source:Integral)->List[Integral]:
            """
            In:
                *source : Integral : source vertex
            Out:
                *List[Integral] : path that has the highest pheromones
            This function creates a path that has the highest pheromones not considering the weights
            """
            path:List[Integral]=[source]
            vertex_seen:dict[Integral,str]={source:"already seen"}
            while len(path) < len(graph.vertices):
                max_path=float("-inf")
                for vertex in graph.vertices:
                    if vertex!= path[-1]:
                        if not vertex in vertex_seen and pheromones [vertex][path[-1]]>max_path:
                            max_path=pheromones [vertex][path[-1]]
                            ville=vertex
                vertex_seen[ville]="already seen"
                path.append(ville)
            return path
        

        def aco( evaporation:float, alpha:float, beta:float,ant:int,source:Integral,p)->List[Integral]:
            """
            In:
                *evaporation : float : evaporation rate
                *alpha : float : coefficient of the importance of pheromones
                *beta : float : coefficient of the importance of weights
                *ant : int : number of ants
                *source : Integral : source vertex
                *p : float : probability of having an elitist ant
            Out:
                *List[Integral] : path with the highest pheromones
            This function creates the shortest path using the ant colonies optimization
            """
            for _ in range(ant):
                path:List[Integral]=ant(alpha, beta,source)
                drop_pheromones(path)
                evapore_pheromones(evaporation)
                if random()<p:
                    drop_pheromones(glouton_max(source)) #une fois sur 10 c'est une fourmi elitiste -on rajoute des pheromones pour le meilleur chemin(=fourmis élitistes)

            return glouton_max(source)
        
        
        path:List[Integral]=aco(0.1, self.alpha, self.beta,self.ant_nb,source,self.p)
        return path


    

    




    

       
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
        normalisation=self.graph_normalisation(graph)
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
