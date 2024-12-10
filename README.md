# Notas

Proyecto realizado a lo largo de todo el cuatri, en su mayoría realice el código por mi cuenta con mi amigo [Joaco](https://github.com/BA73C0) (siendo que era un tp de a 5)

Me dejó ver la dificultad de montar un proyecto medianamente "grande" (que de todas formas está lejos de serlo)

## Features que me gustaría agregar en un futuro

- Poder tener miembros de grupo que no sean usuarios: deberia cambiar el modelado de la BDD, cambiar como es la aceptación de una invitación ahora mismo, entre otras cosas.
- Carga de fotos por usuarios, o utilización de fotos predeterminadas (estilo Netflix): si es la segunda opción, no deberia ser algo muy complicado, en un rato lo podría hacer.
- Pago a través de billeteras virtuales: feature más ambiciosa, entiendo que ligarlo a MP no debería ser **tan** complicado pero ya veremos.
- Elegir divisa del gasto: una pavada en principio.
- Creación y manejo de eventos (único gasto asociado a un grupo de gente): feature también ambiciosa pero por el hecho de tener que dedicarle un tiempo que hoy mismo no tengo.

También me gustaría meter mano y emprolijar y formatear el código, ya que en ciertas partes quedó medio un asco, además de terminar de testear la API.

# Aclaración

Deberias tener un .env en backend y en frontend declarando las variables que se piden en dichos repos.

Proximamente agrego algunos de ejemplo para que cualquiera la pueda utilizar

# RUN

1. Te paras sobre la carpeta /backend y activas el virtual environment con

`source venv/bin/activate`

recien ahi instalas dependencias con

`pip install -r requirements.txt`

y ahi corres

`uvicorn main:app --reload`

2. Te paras sobre la carpeta /frontend y corres con `npm run dev`

# App en uso

![Captura desde 2024-12-09 22-42-15](https://github.com/user-attachments/assets/9eb9d70c-5d60-4f23-8063-e91be982f246)

![Captura desde 2024-12-09 22-42-08](https://github.com/user-attachments/assets/73c8d741-ca36-4434-ac5d-75043cb03429)

![Captura desde 2024-12-09 22-42-22](https://github.com/user-attachments/assets/20ba4068-72cb-463d-811f-76b75935fede)

![Captura desde 2024-12-09 22-42-33](https://github.com/user-attachments/assets/0f579fc5-14d3-445c-9a38-cb2f47a39624)

![Captura desde 2024-12-09 22-42-56](https://github.com/user-attachments/assets/7e2d7964-1312-4586-86eb-ebdfdc249fb2)

![Captura desde 2024-12-09 22-42-45](https://github.com/user-attachments/assets/e1fedbe5-1efd-4a3f-bdd4-eb246703db76)

![Captura desde 2024-12-09 22-43-17](https://github.com/user-attachments/assets/21255be5-9cf0-435f-888d-5ce0c050e408)

