Feature: Agregar gastos

  Scenario: Agregar gastos sin ser parte de un evento/grupo
    Given no soy parte de un evento/grupo
    When agrego mis gastos 
    Then no agrego mis gastos

  Scenario: Agregar gastos siendo el único participante
    Given soy parte de un evento/grupo en el que soy el único participante
    When agrego mis gastos siendo el único integrante
    Then mi saldo actual sigue siendo el previo

  Scenario: Agregar gastos siendo parte de un evento/grupo con más participantes
    Given soy parte de un evento/grupo en el que hay más de un participante
    When agrego que realicé un gasto de X
    Then el gasto del grupo aumenta en X