Feature: Inicio de sesion

Scenario: No estoy registrado
    Given no estoy registrado
    When inicio sesión
    Then no puedo iniciar sesión porque no estoy registrado

Scenario: Estoy registrado e ingreso mal la contraseña
	Given estoy registrado
	When quiero iniciar sesión e ingreso mal mi contraseña
	Then no puedo iniciar sesión

Scenario: Estoy registrado e ingreso bien la contraseña
	Given estoy registrado
	When quiero iniciar sesión e ingreso bien mi contraseña	
	Then puedo iniciar sesión
