import aima_libs.hanoi_states as hanoi_states
from aima_libs.tree_hanoi import NodeHanoi

class DFS:
    """
    Clase para resolver el problema de la Torre de Hanoi usando Búsqueda Primero en Profundidad (DFS).
    """

    def __init__(self, number_disks: int = 5):
        """
        Inicializa DFS.

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

    def depth_first_search(self):
        frontier = [NodeHanoi(self.problem.initial)] # Stack LIFO con el nodo inicial
        explored = set() # Conjunto de estados ya visitados
        self.nodes_explored = 0
        self.max_depth_reached = 0

        while frontier: # while len(frontier) != 0
            node = frontier.pop()
            self.nodes_explored += 1
            
            if node.depth > self.max_depth_reached:
                self.max_depth_reached = node.depth
            
            if node.state in explored:
                continue
            
            explored.add(node.state)
            
            if self.problem.goal_test(node.state):
                return node, self._build_metrics(node, explored, frontier, True)
            
            # Agregamos a la frontera los nodos sucesores que no hayan sido visitados
            for child in node.expand(self.problem): #'mueve' y retorna la lista de nodos hijos
                if child.state not in explored and child not in frontier:
                    frontier.append(child)

        # Si no se encuentra solución, devolvemos métricas igualmente
        return None, self._build_metrics(node, explored, frontier, False)
    
    def _build_metrics(self, node, explored, frontier, solution_found):
        return {
            "solution_found": solution_found,
            "nodes_explored": self.nodes_explored,
            "states_visited": len(explored),
            "nodes_in_frontier": len(frontier),
            "max_depth": self.max_depth_reached,
            "cost_total": node.state.accumulated_cost if solution_found else None,
        }
        