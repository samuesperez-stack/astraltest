# TOYP Venezuela 2026 — video completo V3

**20 segundos · vertical 1080 × 1920 · 60 fps · música, sin voz.**

- [Ver / descargar el video completo](TOYP_40_A_10_Completo_V3.mp4?raw=true)
- [Descargar el proyecto editable de Remotion](TOYP_Completo_V3_Proyecto.zip?raw=true)
- [Ver encuadres del MP4 final](TOYP_Completo_V3_Encuadres.jpg)
- [Verificación técnica](verification.json)

La apertura muestra el logo centrado y lo integra en el mosaico. Después aparecen las postulaciones, el giro a caras anónimas y la selección dorada. Las diez tarjetas verticales pasan al carrusel por parejas; siguen el corte a «SOLO 10» y el cierre con fecha, transmisión y contactos.

Los titulares están centrados en el video; las categorías y números, dentro de sus tarjetas. El cierre mantiene el contenido esencial por encima de y=1500, con márgenes laterales, para reducir interferencias con los controles de redes. Las interfaces concretas pueden variar entre plataformas.

Se añadieron 1,5 segundos de apertura y medio segundo de cierre al objetivo inicial de 18 segundos. El MP4 final contiene 1.200 frames. Se verificaron dimensiones, duración, fps, decodificación, sincronización de audio y pico verdadero; se revisaron los encuadres de apertura, giro, escaneo, cinco parejas de categorías, clímax y cierre.

## Editar

Descomprimir el ZIP, entrar en `toyp-mosaico` y ejecutar:

```bash
npm ci --no-audit --no-fund
npm run studio
npm run render:full
```

La composición completa es `ToypFullV3`; Studio usa `http://localhost:3102/ToypFullV3`. El comando de render espera Chromium en `/usr/bin/chromium`. Se incluyen fotos derivadas, fuentes y licencias, mezcla de audio y código reproducible. Se conservan como composiciones independientes la [versión inicial](../README.md) y la [prueba V2](../v2/README.md).

Las 41 fotos únicas aparecen en el muro; las posiciones destacadas son anónimas e ilustrativas, no una lista de ganadores. No se incluyen los originales privados ni el documento de identidad completo. Las categorías se abrevian en pantalla; sus nombres completos están en el proyecto. La identidad usa la marca vectorial del portal oficial, con bajada y año compuestos siguiendo la referencia suministrada.

## Música — conservar al publicar

**Inspired — Kevin MacLeod (incompetech.com)**

Licensed under Creative Commons Attribution 4.0 International:
https://creativecommons.org/licenses/by/4.0/

Fuente oficial: https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1600022

Adaptación: extracto 01:00–01:20, fundidos, ajuste de nivel y efectos originales de obturador, giro, escáner y transiciones. El crédito también aparece al cierre del video.
