Feature: Actualizar grupo

  Scenario: Actualizar siendo un usuario no registrado
    Given no estoy registrado
    When actualizo mi grupo
    Then se me indica que no estoy registrado 

  Scenario: Actualizar siendo un usuario registrado un grupo inexistente
    Given estoy registrado y no existe mi grupo
    When actualizo mi grupo inexistente
    Then se me indica que no existe el grupo

  Scenario: Actualizar siendo un usuario registrado con datos inválidos un grupo existente
    Given estoy registrado y existe mi grupo
    When actualizo mi grupo con datos inválidos
    Then no se actualiza

  Scenario: Actualizar siendo un usuario registrado con datos válidos un grupo existente
    Given estoy registrado y existe mi grupo
    When actualizo mi grupo con datos válidos
    Then se actualiza