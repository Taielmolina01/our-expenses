# backend-we-expenses

## TO DO

- [ ] Test
    - [ ] Agregar tests probando los nuevos endpoints (balance por grupo) (testear caso de usuario en mas de un grupo)
    - [ ] Agregar más tests, los de actualizar y borrar creo que no hicimos nada. (importante !!!!)
    - [ ] Agregar test de pasar mal fecha, y de todo lo que falte
- [ ] Problemas API
    - [ ] Si agrego una deuda con q alguien paga 0, no deberia generarse 
    - [X]  Traducir errores a ingles
    - [X] Tengo que agregar endpoint para deudas por grupo
    - [X] Agregar campos para updatear usuario
    - [ ] Agregar más errores, por ejemplo que un usuario puede agregar a otro a un grupo, solo si pertenece al grupo, solo si esta logeado, etc. REVISAR CODIGO
    - [ ] Corregir status code de errores lanzados

- [ ] Refactor
    - [ ] El código de los tests esta medio ilegible
    - [ ] El codigo de pagar deuda es un asco ahora mismo

## RUN

Tenes que tener el .venv activado  con

`source venv/bin/activate` 

recien ahi instalas dependencias con

`pip install -r requirements.txt`

y ahi corres

`uvicorn main:app --reload`

## TEST

Te paras sobre la carpeta padre y corres

`pytest`

si queres correr uno en particular es

`pytest tests/test_a_probar.py`


