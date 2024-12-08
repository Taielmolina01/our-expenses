Feature: Creación de grupos

Scenario: Crear un grupo sin estar registrado
	Given que no tengo una sesión iniciada
	When creo un grupo
	Then no se crea el grupo

Scenario: Crear un grupo sin nombre
	Given que tengo una sesión iniciada
	When creo un grupo sin nombre
	Then no se crea el grupo

Scenario: Crear un grupo con nombre
	Given que tengo una sesión iniciada
	When creo un grupo con nombre
	Then se crea el grupo

