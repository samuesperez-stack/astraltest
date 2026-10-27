# CHEKI V3 — Freezer Vice / one-take animado

## Descargar
- [Video V3 completo · 1080×1920 / 30 fps / 42,9 s](https://github.com/samuesperez-stack/astraltest/raw/refs/heads/cheki-freezer-deliverables/deliverables/cheki-freezer/v3/CHEKI_OneTake_V3.mp4)
- [Proyecto editable V3 y todos los recursos](https://github.com/samuesperez-stack/astraltest/raw/refs/heads/cheki-freezer-deliverables/deliverables/cheki-freezer/v3/CHEKI_Proyecto_V3.zip)
- [Extracto del recorrido · 18–26 segundos](https://github.com/samuesperez-stack/astraltest/raw/refs/heads/cheki-freezer-deliverables/deliverables/cheki-freezer/v3/CHEKI_V3_Recorrido_18-26.mp4)
- [Vista del recorrido completo](CHEKI_V3_Contact_Sheet.jpg)

## Dirección
Una cámara continua atraviesa un freezer imposible: puertas con bisagras, estantes, latas suspendidas, personaje, cristales, monitor de IlloJuan, cámara baja, segundo personaje, corona, meme de codificación y arco de salida. Se conservan los cameos pedidos y se incorporan rótulos de HOTEL MALIGNO / MARBELLA VICE como guiños al contexto musical descrito en las [fuentes consultadas](V3_RESEARCH.md).

Es un one-take simulado con escenario 3D y personajes/objetos fotográficos 2.5D, no una grabación real. Los cameos son ilustraciones, no clips auténticos. La procedencia del meme no se ha verificado. La letra conserva las 16 líneas del usuario, con cues vocales todavía aproximados y no revisados a oído.

Las frases se distribuyen en un máximo de dos filas y salen antes del siguiente cue. El monitor se abre para dejar pasar la cámara y los rótulos se elevan durante el cierre. La [dirección y método](V3_DIRECTION.md) están documentados.

## Verificación
La copia de entrega pasa decodificación completa, 1287 frames, duración a menos de un frame del audio y comparación de posición con el original. Se verificó continuidad de las poses de cámara y movimiento de los frames, sin tramos negros inesperados o secuencias congeladas de cuatro frames. Son comprobaciones técnicas, no una aprobación de sincronía vocal.

El máster nativo superó el límite de archivo de GitHub y se conservó en el entorno. Esta descarga tiene compresión H.264 adicional CRF 25, mantiene 1080×1920/30 fps y copia el audio sin recodificar; puede perder detalle fino frente al máster. El código permite regenerar ambos.

## Proyecto
Descomprimir ZIP, entrar en `cheki-freezer/remotion`, ejecutar `npm ci` y `npm run studio`. Para exportar: `npm run render`. Requiere Node 24, Chromium con WebGL/SwiftShader y FFmpeg. Ajustar `/usr/bin/chromium` si se usa otra máquina. No hacen falta APIs o recursos remotos tras instalar dependencias.

V1 y V2 se mantienen en las carpetas superiores. `CHEKI_V3_Camera_Test.mp4` y las dos imágenes PNG son pruebas iniciales de la trayectoria anteriores a los últimos ajustes; el MP4 completo y la hoja de contacto reflejan la versión final corregida. Procedencia, fuentes y licencias se incluyen en el ZIP.
