Feature: Eliminar grupo

  Scenario: Borrar grupo siendo un usuario no registrado
    Given no estoy registrado
    When elimino un grupo
    Then no se elimina

  Scenario: Borrar grupo siendo usuario registrado no siendo parte del grupo
    Given estoy registrado
    When elimino un grupo en el que no soy parte
    Then se me indica que no pertenezco al grupo

  Scenario: Borrar grupo siendo usuario registrado siendo parte del grupo
    Given estoy registrado
    When elimino un grupo en el que soy parte
    Then se elimina