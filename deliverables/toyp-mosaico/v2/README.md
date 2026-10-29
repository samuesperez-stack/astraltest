# TOYP — prueba de dirección V2

Prueba de **6,5 segundos**, vertical **1080 × 1920 / 60 fps**, con música y sin voz. Revisa el inicio del video a partir del MD original: muro fotográfico completo → frenado → giro a caras anónimas → escaneo dorado → diez posiciones elevadas.

- [Ver / descargar la prueba MP4](TOYP_Mosaico_Prueba_V2.mp4?raw=true)
- [Descargar el proyecto editable](TOYP_Mosaico_Prueba_V2_Proyecto.zip?raw=true)
- [Ver hoja de encuadres](TOYP_Prueba_V2_Encuadres.jpg)
- [Verificación técnica](verification.json)
- [Comprobación geométrica del encuadre](geometry-review.json)

El video completo sigue previsto en 18 segundos. Esta prueba comprende únicamente el muro y la selección; el carrusel de tarjetas, «SOLO 10» y el cierre institucional se desarrollan después. La [versión inicial](../README.md) se conserva para comparar.

Se utilizan las 41 fotografías únicas recibidas y una celda de marca. Todas las celdas ocultan su retrato antes de que aparezca el primer borde de selección. Las diez posiciones anónimas son ilustrativas: no identifican ganadores reales. El documento de identidad original se excluye; solo se incluye su recorte facial derivado.

Los retratos mantienen su proporción durante el giro; la elevación conserva la misma geometría de tarjeta. Los textos de la fase de selección se sitúan fuera de la fila activa del escáner. Se revisaron encuadres de inicio, giro, escaneo y reposo final.

## Ejecutar el proyecto

Descomprimir el ZIP, entrar en `toyp-mosaico` y ejecutar:

```bash
npm ci --no-audit --no-fund
npm run typecheck
npm run render:proof
```

Requiere Node y Chromium; el comando usa `/usr/bin/chromium`. La composición nueva se llama `ToypMosaicProofV2`. Se incluyen las fuentes con sus licencias, fotos derivadas, música, mezcla y scripts reproducibles. Los originales privados, dependencias instaladas y caché de compilación no se incluyen.

## Música — conservar al compartir

**Inspired — Kevin MacLeod (incompetech.com)**

Licensed under Creative Commons Attribution 4.0 International:
https://creativecommons.org/licenses/by/4.0/

Fuente oficial: https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1600022

Adaptación: extracto 01:00–01:06,5, fundidos, nivelado y efectos originales de obturador, giro, escáner y selección. Esta atribución acompaña el MP4 de prueba; no hay créditos sobreimpresos en sus 6,5 segundos.
