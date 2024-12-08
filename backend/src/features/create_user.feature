Feature: Registro de usuario

Scenario: Registro con un email existente
  Given no estoy registrado
  When me quiero registrar con un email que ya existe previamente
  Then no puedo registrarme en la aplicación

Scenario: Registro con un email inexistente
  Given no estoy registrado
  When tengo un email válido e ingreso la contraseña deseada y la confirmo
  Then puedo registrar mi usuario y contraseña en la aplicación