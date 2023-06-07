import numpy as np

class Node:
    def __init__(self, level, value, pruned_type, solution):
        self.level = level  # Nível do nó na árvore de busca
        self.value = value  # Valor do nó
        self.pruned_type = pruned_type  # Tipo de poda do nó
        self.solution = solution  # Solução associada ao nó

def branch_and_bound(c, A, b):
    n = len(c)
    best_solution = None  # Melhor solução encontrada
    best_value = float('-inf')  # Melhor valor encontrado
    active_nodes = []  # Lista de nós ativos

    # Cria o nó raiz e o adiciona à lista de nós ativos
    root_node = Node(0, 0, None, [0] * n)
    active_nodes.append(root_node)

    while active_nodes:
        node = active_nodes.pop()

        print_node(node)  # Imprime o nó atual

        if node.level == n:
            # Se o nível do nó for igual ao número de variáveis, chegamos a uma solução completa
            # Verifica se a solução atual é a melhor encontrada até agora
            if node.value > best_value:
                best_solution = node.solution
                best_value = node.value
            continue

        x = np.array(node.solution)
        x[node.level] = 1
        if is_feasible(x, A, b):
            # Se atribuir 1 à variável atual for factível, cria um novo nó com essa atribuição e o adiciona à lista de nós ativos
            value = np.dot(c, x)
            if value > best_value:
                best_value = value
                best_solution = x.tolist()
            active_nodes.append(Node(node.level + 1, value, None, x.tolist()))
            print_tree_node(node.level + 1, '├──', x.tolist())

        x[node.level] = 0
        if is_feasible(x, A, b):
            # Se atribuir 0 à variável atual for factível, cria um novo nó com essa atribuição e o adiciona à lista de nós ativos
            value = np.dot(c, x)
            if value > best_value:
                best_value = value
                best_solution = x.tolist()
            # Verifica se o nó pode ser podado
            if value <= best_value:
                active_nodes.append(
                    Node(node.level + 1, value, "Upper Bound", x.tolist()))
                print_tree_node(node.level + 1, '└──', x.tolist())

    return best_solution, best_value

def is_feasible(x, A, b):
    # Verifica se a solução x é factível em relação às restrições lineares representadas por A e b
    return np.all(np.dot(A, x) <= b)

def read_input(filename):
    # Lê o arquivo de entrada e retorna os valores necessários para o problema
    with open(filename, 'r') as file:
        lines = file.readlines()
        num_vars, num_constraints = map(int, lines[0].strip().split())
        c = list(map(int, lines[1].strip().split()))
        A = []
        b = []
        for i in range(2, num_constraints + 2):
            constraint = list(map(int, lines[i].strip().split()))
            A.append(constraint[:-1])
            b.append(constraint[-1])
        return c, np.array(A), np.array(b)

def print_node(node):
    # Imprime informações sobre o nó atual
    print(f"Nível: {node.level}, Valor: {node.value}")

def print_tree_node(level, connector, value):
    # Imprime informações sobre um nó na forma de uma árvore
    indent = '    ' * level
    fract_value = [f'x[{i}] = {val}' if val % 1 != 0 else f'x[{i}] = {int(val)}' for i, val in enumerate(value)]
    print(f'{indent}{connector}{", ".join(fract_value)}')

c, A, b = read_input('teste2.txt')

# Relaxação linear
relaxed_solution = np.linalg.lstsq(A, b, rcond=None)[0].tolist()
relaxed_value = np.dot(c, relaxed_solution)

print("Solução Relaxada:")
for i, val in enumerate(relaxed_solution):
    print(f'x[{i}] = {val}')
print("Valor Relaxado:")
print(relaxed_value)

# Executa o Branch and Bound
best_solution, best_value = branch_and_bound(c, A, b)

print("\nValor da solução ótima:", best_value)
