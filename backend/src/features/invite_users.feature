Feature: Invitación de usuarios

Scenario: Invitar amigos sin estar con sesión iniciada
  Given que no tengo una sesión iniciada
  When invito a mi grupo a mis amigos
  Then no los invito

Scenario: Invitar amigos no registrados
  Given que tengo una sesión iniciada
  When invito a mi grupo a mis amigos por emails no registrados
  Then no los puedo invitar

Scenario: Invitar amigos registrados
  Given que tengo una sesión iniciada
  When invito a mi grupo a mis amigos por emails registrados
  Then los invito