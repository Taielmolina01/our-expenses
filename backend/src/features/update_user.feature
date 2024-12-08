Feature: Actualización de usuario

Scenario: Actualizar un usuario inexistente
  Given no estoy registrado
  When actualizo mi perfil
  Then se me indica que no existe el usuario

Scenario: Actualizar un usuario existente con datos inválidos
  Given estoy registrado
  When actualizo mi perfil con datos inválidos
  Then no se actualiza
  
Scenario: Actualizar un usuario existente con datos válidos
  Given estoy registrado
  When actualizo mi perfil con datos válidos
  Then se actualiza