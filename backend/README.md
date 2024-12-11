# backend-we-expenses

## TO DO

- [ ] Test
    - [ ] Agregar tests probando los nuevos endpoints (balance por grupo) (testear caso de usuario en mas de un grupo)
    - [ ] Agregar más tests, los de actualizar y borrar creo que no hicimos nada. (importante !!!!)
    - [ ] Agregar test de pasar mal fecha, y de todo lo que falte
- [ ] Problemas API
    - [ ] Si agrego una deuda con q alguien paga 0, no deberia generarse 
    - [ ] Agregar más errores, por ejemplo que un usuario puede agregar a otro a un grupo, solo si pertenece al grupo, solo si esta logeado, etc. REVISAR CODIGO
    - [ ] Corregir status code de errores lanzados

- [ ] Refactor
    - [ ] El código de los tests esta medio ilegible
    - [ ] El codigo de pagar deuda es un asco ahora mismo

## RUN

Hay que tener python instalado
### WINDOWS
#### Paso 1

Navegar hasta estar dentro de la carpeta del proyecto y ejecutar

`python -m venv .venv` 

para crear un entorno virtual

#### Paso 2

Activar el entorno creado

`.venv\Scripts\activate` 

### LINUX

#### Paso 1

Navegar hasta estar dentro de la carpeta del proyecto y ejecutar

`python3 -m venv .venv` 

para crear un entorno virtual

#### Paso 2

Activar el entorno creado

`source .venv/bin/activate` 

### igual para ambos OS

#### Paso 3

Instalar las dependencias

`pip install -r requirements.txt`

#### Paso 4

Generar un archivo .env con los mismos datos, o cambiando a gusto los proporcionados en .env.mock

#### Paso 4

Ejecutar

`uvicorn main:app --reload`

para iniciar el servidor

#### Paso 5

Para cerrar el entorno virtual al finalizar, ejecutar 

`deactivate`

## TEST

Navegar hasta estar dentro de la carpeta del proyecto y ejecutar

`pytest` 

Para ejecutar uno en particular ejecutar

`pytest tests/test_a_probar.py`
