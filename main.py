from mip import Model, xsum, maximize, BINARY


def branch_and_bound(c, A, b):
  # Inicialização
  best_obj = float('-inf')
  best_solution = None
  open_nodes = []
  all_branches = []  # Lista para armazenar todas as ramificações feitas

  # Criar o nó raiz
  root = {
    'lower_bound': float('-inf'),
    'upper_bound': float('inf'),
    'solution': []
  }
  open_nodes.append(root)

  while open_nodes:
    # Selecionar próximo nó a ser resolvido
    node = open_nodes.pop()

    # Verificar se o nó precisa ser resolvido
    if node['lower_bound'] > best_obj:
      continue

    # Criar modelo para resolver o subproblema linear
    model = Model()

    # Variáveis binárias
    x = [model.add_var(var_type=BINARY) for _ in range(len(c))]

    # Função objetivo
    model.objective = maximize(xsum(c[i] * x[i] for i in range(len(c))))

    # Restrições
    for j in range(len(A)):
      model += xsum(A[j][i] * x[i] for i in range(len(c))) <= b[j]

    # Resolver o subproblema linear
    model.optimize()

    # Verificar se a solução é inteira
    if model.num_solutions:
      obj = model.objective_value
      solution = [int(x[i].x) for i in range(len(c))]

      # Atualizar a melhor solução encontrada
      if obj > best_obj:
        best_obj = obj
        best_solution = solution

    # Verificar se a solução é fracionária
    if any(not x[i].x.is_integer() for i in range(len(c))):
      # Encontrar variável mais fracionária
      frac_var = max(range(len(c)), key=lambda i: abs(x[i].x - 0.5))

      # Ramificar em dois nós filhos
      node_1 = {
        'lower_bound': node['lower_bound'],
        'upper_bound': node['upper_bound'],
        'solution': node['solution'] + [(frac_var, 1)]
      }
      node_2 = {
        'lower_bound': node['lower_bound'],
        'upper_bound': node['upper_bound'],
        'solution': node['solution'] + [(frac_var, 0)]
      }

      # Atualizar limites dos nós filhos
      node_1['lower_bound'] = max(node_1['lower_bound'], best_obj)
      node_2['lower_bound'] = max(node_2['lower_bound'], best_obj)

      open_nodes.append(node_1)
      open_nodes.append(node_2)

      # Armazenar as ramificações feitas
      all_branches.append(node_1)
      all_branches.append(node_2)

  return best_obj, best_solution, all_branches


# Função para ler os dados do arquivo
def read_input_file(filename):
  with open(filename, 'r') as file:
    num_vars, num_constraints = map(int, file.readline().split())
    c = list(map(int, file.readline().split()))
    A = []
    b = []
    for _ in range(num_constraints):
      line = list(map(int, file.readline().split()))
      A.append(line[:-1])
      b.append(line[-1])
  return c, A, b


# Exemplo de uso
filename = 'teste4.txt'  # Nome do arquivo de entrada
c, A, b = read_input_file(filename)
best_obj, best_solution, all_branches = branch_and_bound(c, A, b)

# Imprimir a solução ótima
print("Melhor objetivo:", best_obj)
print("Melhor solução:", best_solution)
