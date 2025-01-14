from pulp import LpProblem, LpMaximize, LpVariable, lpSum, GLPK
import sys

def read_data(factories, countries, children) -> None:
   
   n, m, t = map(int, input().split())
   factories_aux = {}

   for _ in range(m):
      countries.append({'id': 0, 'export_limit': 0, 'min_distribute': 0, 'factories': [], 'children': []})


   ids_validos = set()

   # Dados das fábricas
   for _ in range(n):
      factory_id, country_id, stock = map(int, sys.stdin.readline().split())

      if stock > 0:
         ids_validos.add(factory_id)
         factories_aux[factory_id] = {'id': factory_id, 'country_id': country_id, 'stock': stock, 'children': []}
         countries[country_id-1]['factories'].append(factories_aux[factory_id])

   # Dados dos países
   for _ in range(m):
      country_id, export_limit, min_distribute = map(int, sys.stdin.readline().split())
      countries[country_id-1]['id'] = country_id
      countries[country_id-1]['export_limit'] = export_limit
      countries[country_id-1]['min_distribute'] = min_distribute


   # Pedidos das crianças
   for _ in range(t):
      line = list(map(int, sys.stdin.readline().split()))
      child_id, country_id, *factory_ids = line
      clean = [f_id for f_id in factory_ids if f_id in ids_validos]
      if clean:
         child = {'id': child_id, 'country_id': country_id, 'factories': clean}
         children.append(child)
         countries[country_id-1]['children'].append(child)
         for factory_id in clean:
            factories_aux[factory_id]['children'].append(child)

   factories.extend(factories_aux.values())


# Função para resolver o problema
def solve_toy_distribution() -> int:
   # Dados do problema
   factories, countries, children = [], [], []

   # Ler os dados do arquivo
   read_data(factories, countries, children)

   # Criar o modelo de otimização
   model = LpProblem("Toy_Distribution", LpMaximize)

   # Variáveis de decisão
   x = {(child['id'], factory_id): LpVariable(f"x_{child['id']}_{factory_id}", cat="Binary")
        for child in children for factory_id in child['factories']}

   # Função objetivo
   model += lpSum(x[k, i] for k, i in x), "Maximize Children Satisfied"

   # Restrições
   # 1. Um brinquedo por criança
   for child in children:
      model += lpSum(x[child['id'], i] for i in child['factories']) <= 1, f"One_Per_Child_{child['id']}"

   # 2. Stock máximo das fábricas
   for factory in factories:
      if factory['children']:
         model += lpSum(x[child['id'], factory['id']] for child in factory['children']) <= factory['stock'], f"Stock_Factory_{factory['id']}"

   for country in countries:
      # 3. Distribuição mínima por país
      if country['children']:
         internal_toys = lpSum(
            x[child['id'], i] 
            for child in country['children']
            for i in child['factories']
         )
         model += internal_toys >= country['min_distribute'], f"Min_Distribute_Country_{country['id']}"

      # 4. Limite de exportação por país
      if country['factories']:
         exports = lpSum(
            x[child['id'], factory['id']]
            for factory in country['factories']
            for child in factory['children'] if child['country_id'] != country['id']
         )
         model += exports <= country['export_limit'], f"Export_Limit_Country_{country['id']}"
    
   # Resolver o modelo
   model.solve(GLPK(msg=0))

   # Retornar resultado
   if model.status == 1:  # Solução ótima encontrada
      return int(model.objective.value())
   else:
      return -1

# Executar a função principal e imprimir o resultado
if __name__ == "__main__":
   result = solve_toy_distribution()
   print(result)
