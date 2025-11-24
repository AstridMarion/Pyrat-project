"""
    This file contains useful elements to define a particular player.
    In order to use this player, you need to instanciate it and add it to a game.
    Please refer to example games to see how to do it properly.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
from numbers import *
from Dijkstra import Dijkstra

# PyRat imports
from pyrat import Player, Maze, GameState, Action,Graph

#####################################################################################################################################################
###################################################################### CLASSE ######################################################################
#####################################################################################################################################################

class Exhaustive (Player):

    """
        This player is basically a player that traverses the graph associated with the game 
        using a TSP with the positions of the cheeses and the initial position of the mouse 
        as vertices.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:     Self,
                   *args:    Any,
                   **kwargs: Any
                 ) ->        Self:

        """
            This function is the constructor of the class.
            When an object is instantiated, this method is called to initialize the object.
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
        graph,graph_return=self.maze_to_graph(maze,game_state)
        route=self.route_mouse(self.TSP(graph,game_state.player_locations[self.name]),graph_return)
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

#####################################################################################################################################################
#                                                        OTHER METHODS                                                               #
#####################################################################################################################################################
    @override
    def maze_to_graph(self:Self, 
                    graph:Graph,
                    game_state:GameState
                    )->Tuple[Graph,Dict[Integral,Dict[Integral,List[Integral]]]] :
        """
            This method performs (nb_cheese + source)**2 Dijkstra traversals of a graph.
            It creates the graph of vertices to explore with associated distances as weights of edges.
            It also returns the table of optimized routes between two vertices.
            In:
                * self:   Reference to the current object.
                * graph:  The graph to traverse.
                * game_state: An object representing the state of the game.
            Out: a Tuple:
                * graph_for_TSP: Graph[]: The graph with the distances between each cheese/source.
                * graph_return: Dict[Integral,Dict[Integral,List[Integral]]]: The routing table of 
                    each optimized path linking every vertex (cheese/initial position)
                    chape of the Dict: {v1:{v2: [list representing the path between v1 and v2]}}
        """

        player=Dijkstra()
        #find location of vertices
        source:Integral=game_state.player_locations[self.name]
        cheeses:List[Integral]=game_state.cheese

        #initialize graph_for_TSP
        graph_for_TSP:Graph=Graph()
        graph_for_TSP.add_vertex(source)
        for cheese in cheeses :
            graph_for_TSP.add_vertex(cheese)

        #initialize graph_return
        graph_return:Dict[Integral,Dict[Integral,List[Integral]]]={source:{}}

        #find path between source and each cheese
        distance,routing_table=player.traversal(graph,source)
        for cheese in cheeses:
            graph_for_TSP.add_edge(source,cheese,distance[cheese],symmetric=True)
            graph_return[source][cheese]=player.find_route(routing_table,source,cheese)
        
        #find path linking each cheese to another cheese
        for cheese in cheeses :
            distance,routing_table=player.traversal(graph,cheese)
            graph_return[cheese]={source:player.find_route(routing_table,cheese,source)}
            for cheese_fin in cheeses:
                if cheese_fin!=cheese: #otherwise the path has a weight = 0
                    graph_for_TSP.add_edge(cheese,cheese_fin,distance[cheese_fin])
                    graph_return[cheese][cheese_fin]=player.find_route(routing_table,cheese,cheese_fin)
        
        return (graph_for_TSP,graph_return)
    

    @override
    def TSP(self:Self,graph:Graph,source:Integral)->List[Integral]:
        """ 
            This method performs a TSP on a graph thanks to the auxiliary 
            fonction boucle.
            It finds the optimized path to visit all the vertices.
            In:
                * graph:  The graph to traverse.
                * source: The initial position of the mouse
            Out:
                * List: The optimized path to visit all the vertices.
        """

        def boucle(path:list[Integral])->Tuple[int,List[Integral]]:
            """ 
                This auxiliary fonction finds the optimized path to visit all the vertices
                In:
                    * path: the optimized path (updated in each recursion)
                Out:
                    * weight_min: the minimal weight of the paths already tested
                    * path_min: the optimized path associated
            """
            #base case
            if len(path)==len(graph.vertices):
                weight=0
                for i in range(len(path)-1):
                    weight+=graph.get_weight(path[i],path[i+1])
                return (weight,path)

            #initialization
            weight_min:float=float('inf')
            path_min:List[Integral]=path

            # build the path by calling the recursive fonction
            for voisin in graph.get_neighbors(path[-1]):
                if not voisin in path: # adds vertex only if he wasn't visited
                    path_new=path.copy()
                    path_new.append(voisin)
                    (weight,path_new_v2)=boucle(path_new)
                    if weight<weight_min: #find the minimum weight
                        weight_min=weight
                        path_min=path_new_v2

            return (int(weight_min),path_min)

        (_,path)=boucle([source])
        return path


    @override
    def route_mouse(self:Self,best_path:List[Integral],graph_return:Dict[Integral,Dict[Integral,List[Integral]]])->List[Integral]:
        """
            This method finds the whole optimized route to visit all the vertices.
            In:
                * self:   Reference to the current object.
                * best_path: The optimized path to visit all the vertices.
                * graph_return: The routing table of each optimized path linking two vertices.
            Out:
                * List: The whole optimized path of the mouse.
        """
        #initialize route
        route:List[Integral]=[best_path[0]]

        #build route with best_path and graph_return
        for i in range(len(best_path)-1):
            route.pop()
            route+=graph_return[best_path[i]][best_path[i+1]]
            
        return route
