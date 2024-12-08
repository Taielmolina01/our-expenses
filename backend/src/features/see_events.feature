Feature: Ver eventos
  Como usuario registrado de la aplicación
  Quiero ver todos los eventos de los que soy parte
  Para hacer un seguimiento de mis gastos

  Scenario: Ver eventos de los que soy parte
    Given soy parte de un evento
    When entre a la aplicación
    Then veo una lista de mis eventos

  Scenario: No tengo eventos
    Given no soy parte de ningún evento
    When entre a la aplicación
    Then veo un mensaje que dice “No tienes eventos”