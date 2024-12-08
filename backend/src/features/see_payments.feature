Feature: Ver gastos de un grupo
  Como usuario perteneciente a un grupo
  Quiero poder ver los gastos de este
  Para saber quién gastó y en qué categoría

  Scenario: Ver gastos de un grupo con gastos
    Given pertenezco a un grupo con gastos
    When veo los gastos del grupo
    Then veo listados los gastos del grupo

  Scenario: Ver gastos de un grupo sin gastos
    Given pertenezco a un grupo sin gastos
    When veo los gastos del grupo
    Then no veo ningún gasto registrado