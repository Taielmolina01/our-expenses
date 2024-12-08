Feature: Creación de eventos

Scenario: Invitar miembros registrados a un evento
  Given estoy registrado en la aplicación
  When invito a mi evento a los miembros por nombres de usuario registrados
  Then los invito
  
Scenario: Invitar miembros no registrados a un evento
  Given estoy registrado en la aplicación
  When invito a mi evento a los miembros por nombres de usuario no registrados
  Then no los invito y me avisa diciendo “no existe ese usuario”