# Simulación y revisión

Pruebas realizadas con bases y credenciales temporales, sin utilizar la base real:

- Móvil 390 × 844: inicio, credenciales incorrectas, perfil, búsqueda, puntuación de 20 fichas, envío final y bloqueo tras recargar.
- Corte de conexión con borrador pendiente, intento de salida, reconexión y sincronización.
- Dos dispositivos: uno edita desconectado y el otro guarda una nota distinta. Se rechaza la sobrescritura y se permite recuperar la nota del servidor tras confirmar que se descarta el borrador local.
- Diez jurados: 200 calificaciones, desempate 5–5, prohibición de cerrar con votos faltantes y rechazo de un segundo voto, seguido de una nueva ronda 6–4 que actualiza el ranking.
- API: acceso administrativo, límite de intentos, origen, perfiles provisionales, versiones, respuesta perdida idempotente, bloqueo, JSON inválido y tamaño, importación y registro de auditoría.
- Vista administrativa móvil: matriz con desplazamiento horizontal, datos y edición bloqueada al iniciar la evaluación.

Los archivos `juror.cjs`, `round.cjs`, `conflict.cjs` y `test_api.py` permiten reproducir las pruebas descritas en `README.md` de esta carpeta. La simulación no equivale a una auditoría independiente, no prueba todos los navegadores ni sustituye las pruebas de la instalación real con HTTPS, copias de seguridad y los 20 postulados definitivos. El respaldo de contingencia se importa bajo responsabilidad de la administración y no tiene firma criptográfica. Si se pierde la respuesta al enviar la evaluación final, el jurado debe reconectarse y comprobar el estado.

## Acceso por código del MD

Se volvieron a ejecutar las simulaciones con los diez códigos (cinco INT y cinco INV) y los dos códigos administrativos del MD. Se mantienen las cuentas y notas internas. Este método **no autentica la identidad** y permite la suplantación de cualquier código conocido; las pruebas funcionales no eliminan ese riesgo.

## Selección final por categorías

Simulación móvil con cuatro categorías ficticias: apertura y cierre, puntuación sin perder el grupo abierto, búsqueda, filtro, recuento y envío definitivo de las 20 fichas. Se verificó el agrupado de variantes de mayúsculas y acentos y el ancho de 320 px. Se probó también edición administrativa en dos categorías, una actualización periódica con cambios pendientes y reagrupación después de guardar. Las categorías visibles en las capturas son ejemplos, no la selección real.
