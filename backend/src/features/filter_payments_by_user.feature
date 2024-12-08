Feature: Filtrar gastos por usuario
  Como usuario perteneciente a un grupo
  Quiero poder ver los gastos de este filtrando por usuario
  Para saber cuánto gastó X y en qué categoría

  Scenario: Filtrar gastos por nombre de usuario
    Given pertenezco a un grupo y existen gastos registrados
    When filtro los gastos por el nombre de un usuario específico
    Then veo una lista de los gastos de ese usuario y las categorías correspondientes

  Scenario: Filtrar gastos por nombre de usuario sin registros
    Given pertenezco a un grupo pero no hay gastos registrados para el usuario seleccionado
    When filtro los gastos por el nombre de ese usuario
    Then no veo ningún gasto y me avisa diciendo “No hay gastos registrados para este usuario”