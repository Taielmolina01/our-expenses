Feature: Filtrar eventos
  Como usuario registrado de la aplicación
  Quiero filtrar los eventos de los que soy parte
  Para hacer un seguimiento de mis gastos

  Scenario: Filtrar eventos por estado
    Given soy parte de varios eventos con estados distintos
    When entre a la aplicación y filtre por estado
    Then veo una lista de mis eventos con ese estado