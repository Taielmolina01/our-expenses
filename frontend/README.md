# frontend-we-expenses

## TO DO

- [ ] Hacer boton para editar pago
- [ ] En el heatmap en el xaxis no se ve en blanco no se porque
- [ ] Rotular ejes heatmap (se supone q lo estoy haciendo pero no funciona)
- [ ] SOBRE LOS ULTIMOS 2: no se aplican los estilos al eje x, ni puta idea por que, en el eje Y estan bien
- [ ] Mover estilos a todos .css, que no queden mismo en el jsx
- [ ] Mover las cosas de app.css a los distintos componentes
- [ ] RESPONSIVE!

## RUN

### Paso 1

Navegar hasta estar dentro de la carpeta del proyecto y ejecutar

`xargs -a dependencies.txt -r -- npm install` || `xargs -a dependencies.txt -r -- yarn add`
&&
`npm install` || `yarn install`

En caso de cambiar el puerto donde se corre el backend deberías actualizar el archivo .env

Finalmente correr

`npm run dev` 

### Paso 2

En el navegador abrir

`http://localhost:5173/` 

Notar que de no tener el backend corriendo no se podrá entrar a la app
