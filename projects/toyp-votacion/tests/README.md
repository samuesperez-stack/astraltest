# Simulaciones

`python tests/test_api.py` necesita httpx (`pip install -r requirements-dev.txt`). Utiliza exclusivamente una base temporal y verifica autorización, preparación de perfiles, versiones, bloqueo, importación y origen.

Las pruebas de navegador se ejecutan solo con `TOYP_TEST_ONLY=YES` y URL localhost. Requieren Playwright instalado para Node y Chromium disponible en `/usr/bin/chromium`. Son destructivas respecto a la base de prueba: crear una base SQLite nueva en `/tmp`, generar credenciales con `setup_access.py`, y preparar sus 20 fichas de ejemplo. Nunca dirigirlas a una instalación real. Establecer `TOYP_TEST_CREDENTIALS` con el archivo de prueba y `TOYP_TEST_URL` con la URL local del servidor de prueba. Ejecutar `node tests/juror.cjs` y luego `node tests/round.cjs` sobre esa misma base; `node tests/conflict.cjs` requiere otra base nueva con las 20 fichas preparadas. Se prueban conexión, reconexión, sesión, 20 notas, dos rondas y conflicto entre dispositivos.
