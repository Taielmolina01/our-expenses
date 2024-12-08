# Notas

Proyecto realizado a lo largo de todo el cuatri, en su gran mayoría realice el código por mi cuenta, con numerosos aportes de mi amigo @Joaco (dsp lo pineo)

Me dejó ver la dificultad de montar un proyecto medianamente "grande" (que de todas formas está lejos de serlo)

## Features que me gustaría agregar en un futuro

- Poder tener miembros de grupo que no sean usuarios: deberia cambiar el modelado de la BDD, cambiar como es la aceptación de una invitación ahora mismo, entre otras cosas.
- Carga de fotos por usuarios, o utilización de fotos predeterminadas (estilo Netflix): si es la segunda opción, no debe:ia ser algo muy complicado, en un rato lo podría hacer.
- Pago a través de billeteras virtuales: feature más ambiciosa, entiendo que ligarlo a MP no debería ser **tan** complicado pero ya veremos.
- Elegir divisa del gasto: una pavada en principio.
- Creación y manejo de eventos (único gasto asociado a un grupo de gente): feature también ambiciosa pero por el hecho de tener que dedicarle un tiempo que hoy mismo no tengo.

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
