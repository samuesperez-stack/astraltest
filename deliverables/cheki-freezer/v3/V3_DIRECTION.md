# V3 — CHEKI / Freezer Vice

## Dirección
La petición actual da libertad para superar el storyboard y crear una versión mucho más dinámica, con sensación de one-take y referencias a Los Diozes. Se sustituye el montaje de escenas discretas por una cámara continua que atraviesa un escenario 3D, manteniendo los colores y el humor de las versiones anteriores.

El enfoque es un recorrido surrealista: congelador, pasillo de latas, personaje, hielo suspendido, monitor de reacción, tramo bajo entre cristales, segundo personaje, corona en el espacio, consola de streaming y salida con nombres. La cámara puede girar y acercarse porque paredes, estantes y puertas tienen geometría real. Los personajes y algunos objetos son elementos fotográficos 2.5D; no son humanos 3D articulados ni hay sincronía labial.

## Ruta continua
`remotion/src/v3/path.ts` define posiciones, puntos de mirada y roll con tiempos explícitos. Se interpola con Hermite cúbico usando derivadas respecto al tiempo: no hay salto de posición entre segmentos. El espacio físico es continuo; los memes se encienden en pantallas del decorado, no en cortes a otra escena.

- 0–3 s: puerta abre y cámara entra.
- 3–9 s: acercamiento lateral al personaje y letras por delante.
- 9–14 s: paso entre bloque de hielo y latas suspendidas; rótulo HOTEL MALIGNO.
- 14–17 s: monitor de IlloJuan y «¿un peri qué?».
- 17–23 s: cámara baja cerca del suelo y cruza una compuerta de cristales.
- 23–30 s: segundo personaje, corona y objetos en distintas profundidades.
- 30–37 s: aproximación al estudio congelado; monitor de «Estoy codificando a máxima calidad» y Xokas.
- 37–42,9 s: arco de nombres, última barra y puerta CHEKI que cierra.

Las posiciones son continuas, pero los cambios de contenido en pantallas y las apariciones de frases son eventos gráficos. Se trata de un one-take simulado por animación, no de una toma de cámara real.

## Letras
Cada palabra es una malla con textura de tipografía local. La frase sigue parcialmente la cámara para conservar la lectura, con relieve, resaltado y movimiento al retirarse. El texto conserva la transcripción exacta del usuario; los cues siguen siendo editoriales y no se ha validado alineación vocal palabra por palabra.

## Referencias
Se conserva el cameo ilustrado de IlloJuan, el meme de codificación con Xokas y los nombres pedidos. HOTEL MALIGNO y MARBELLA VICE aparecen como guiños en la arquitectura, apoyados por la fuente descrita en V3_RESEARCH.md. No se han copiado fotogramas oficiales ni añadido voz sintética.

## Implementación
Three.js 0.180.0 dentro de Remotion, con WebGL/SwiftShader (`--gl=swangle`). Render nativo de 1080×1920. Instancias para estantes, latas y cristales; dos luces locales que acompañan la cámara y materiales/texturas locales. La máquina tiene cuota de 4 CPU; se eligen dos workers para el render 3D. La prueba sirvió para corregir iluminación, espaciado y coste de luces antes del render completo.

## Entrega
El render nativo se conserva como máster si supera el tamaño admitido para subirlo a GitHub. Un paso FFmpeg prepara la copia de entrega, sin reducir resolución ni fps y copiando el audio existente. La compresión de entrega es adicional y puede perder detalle fino respecto al máster; el código conserva la posibilidad de regenerar ambos.

## Revisión de calidad del recorrido completo
La primera exportación sirvió para detectar dos defectos que no aparecían en las pruebas puntuales: frases consecutivas que coincidían visualmente al retirarse, y el paso de la cámara por el panel del monitor. Se corrigieron en el código antes de la entrega: solo un cue de letra puede ser visible a la vez, el texto se distribuye en un máximo de dos filas y el monitor pivota para abrir paso. Los rótulos de créditos se elevan al acercarse la cámara para que no tapen el cierre.

Las grandes superficies del pasillo usan materiales de textura con iluminación incorporada; los cristales y elementos metálicos conservan luces locales. Esto reduce el coste del render por software manteniendo geometría, perspectiva y resolución nativas. La cámara y los eventos siguen dependiendo únicamente del frame.
