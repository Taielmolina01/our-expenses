Feature: Filtrar gastos por categoría
  Como usuario perteneciente a un grupo
  Quiero poder ver los gastos de este filtrando por categoría
  Para saber cuánto gastamos los pertenecientes al grupo en dicha categoría

  Scenario: Filtrar gastos por una categoría específica
    Given pertenezco a un grupo y hay gastos registrados
    When filtro los gastos por una categoría específica (ej: comida, transporte)
    Then veo una lista de los gastos en esa categoría

  Scenario: Filtrar gastos por categoría sin registros
    Given pertenezco a un grupo pero no hay gastos en la categoría seleccionada
    When filtro los gastos por esa categoría
    Then no veo ningún gasto y me avisa diciendo “No hay gastos registrados en esta categoría”