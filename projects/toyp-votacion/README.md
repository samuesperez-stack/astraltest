# TOYP · Panel de evaluación

Aplicación móvil para evaluar 20 perfiles mediante 10 cuentas de jurado y una cuenta administrativa. Las 20 fichas se crean como **marcadores provisionales**; la organización debe introducir los postulados correctos en el panel administrativo antes de la primera calificación. No se seleccionaron arbitrariamente 20 personas de las fotos recibidas.

## Inicio local

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python setup_access.py --output /ruta/privada/credenciales-toyp.txt
uvicorn app:app --host 127.0.0.1 --port 8000
```

Abre http://localhost:8000. Guarda el archivo de credenciales de forma privada; se genera una sola vez, contiene once contraseñas aleatorias, y no se incluye en el repositorio. `TOYP_DB` permite ubicar SQLite fuera del directorio de la aplicación. Para una instalación accesible por internet se necesita un servidor persistente con HTTPS; usa `TOYP_HTTPS=1` tras configurar HTTPS y realiza copias de seguridad protegidas de la base. No usar GitHub Pages como servidor de votos.

Cada jurado puntúa del 1 al 10 y el envío definitivo exige los 20 perfiles y bloquea cambios mediante una transacción. La administración ve exclusivamente notas enviadas, ranking por suma y distribución de 10 a 1, matriz, progreso, exportación CSV y una segunda votación por grupo empatado. Si la segunda vuelta también empata, se indica como pendiente; no existe voto de calidad. Las rondas solo pueden abrirse cuando los 10 jurados finalizaron. En caso de conexión interrumpida, se conserva un borrador pendiente en el navegador; el envío final requiere confirmación del servidor.

Los perfiles son editables antes del primer voto e incluyen foto, nombre, categoría, trayectoria y las cinco secciones del MD. Los nombres reales de jurados aún requieren datos. El respaldo JSON contiene notas sensibles y debe entregarse por un canal privado. La importación administrativa exige verificar la procedencia del archivo: no tiene firma criptográfica. La acción queda registrada en la base y nunca sobrescribe un envío final. Los resultados son sensibles: no se debe publicar la base ni las credenciales.
