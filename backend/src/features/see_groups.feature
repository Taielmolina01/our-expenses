Feature: Ver grupos
  Como usuario registrado de la aplicación
  Quiero ver todos los grupos de los que soy parte
  Para hacer un seguimiento de mis gastos

  Scenario: Ver grupos de los que soy parte
    Given soy parte de un grupo
    When entre a la aplicación
    Then veo una lista de mis grupos con mis balances de cada uno

  Scenario: No tengo grupos
    Given no soy parte de ningún grupo
    When entre a la aplicación
    Then veo un mensaje que dice “No tienes grupos”