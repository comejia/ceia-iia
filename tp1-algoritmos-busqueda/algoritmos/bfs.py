import aima_libs.hanoi_states as hanoi_states
from aima_libs.tree_hanoi import NodeHanoi

class BFS:
    """
    Clase para resolver el problema de la Torre de Hanoi usando Búsqueda Primero en Anchura (BFS).
    """

    def __init__(self, number_disks: int = 5):
        """
        Inicializa BFS.

        Args:
            number_disks (int): Número de discos.
        """

        self.number_disks = number_disks
        self.problem = self._initialize_problem()
        self.nodes_explored = 0
        self.max_depth_reached = 0

    def _initialize_problem(self):
        list_disks = [i for i in range(self.number_disks, 0, -1)]
        initial_state = hanoi_states.StatesHanoi(list_disks, [], [], max_disks=self.number_disks)
        goal_state = hanoi_states.StatesHanoi([], [], list_disks, max_disks=self.number_disks)
        return hanoi_states.ProblemHanoi(initial=initial_state, goal=goal_state)

    def breadth_first_search(self):

        frontier = [NodeHanoi(self.problem.initial)] # Cola FIFO con el nodo inicial
        explored = set() # Conjunto de estados ya visitados

        node_explored = 0
        
        while len(frontier) != 0:
            node = frontier.pop()
            node_explored += 1
            
            explored.add(node.state) # Verificamos si llegamos al objetivo
            
            if self.problem.goal_test(node.state):
                metrics = {
                    "solution_found": True,
                    "nodes_explored": node_explored,
                    "states_visited": len(explored),
                    "nodes_in_frontier": len(frontier),
                    "max_depth": node.depth,
                    "cost_total": node.state.accumulated_cost,
                }
                return node, metrics
            
            # Agregamos a la frontera los nodos sucesores que no hayan sido visitados
            for next_node in node.expand(self.problem):
                if next_node.state not in explored:
                    frontier.insert(0, next_node)
                    

        # Si no se encuentra solución, devolvemos métricas igualmente
        metrics = {
            "solution_found": False,
            "nodes_explored": node_explored,
            "states_visited": len(explored),
            "nodes_in_frontier": len(frontier),
            "max_depth": node.depth, # OBS: Si no se encontró la solución, este valor solo tiene sentido en breadth_first_search, en otros casos se debe ir llevando registro de cual fue la máxima profundidad
            "cost_total": None,
        }
        return None, metrics