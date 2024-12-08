Feature: Ver balance

  Scenario: Ver balances sin estar con sesión iniciada
    Given no tengo sesión iniciada
    When quiero ver mis balances
    Then no veo mis balances

  Scenario: Ver balances sin ser parte de un grupo
    Given no soy parte de un evento/grupo
    When observo mis balances
    Then no veo ninguno

  Scenario: Ver balances siendo el único integrante de un grupo
    Given soy parte de un evento/grupo en el que soy el único participante
    When veo mi balance
    Then veo que mi balance es 0 siempre

  Scenario: Ver balances siendo parte de varios grupos
    Given soy parte de mas de un evento/grupo
    When veo mis balances
    Then los veo