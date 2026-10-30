# TOYP · selección final y categorías

[Proyecto editable](TOYP_Panel_Proyecto_V4.zip?raw=true) · [Presentación móvil](TOYP_Seleccion_Final_Movil.png) · [Categorías](TOYP_Categorias_Movil.png) · [Categoría abierta](TOYP_Categoria_Abierta_Movil.png) · [Código fuente](../../../projects/toyp-votacion/)

Diseño de selección final con grupos desplegables por categoría para jurado y administración. Cada grupo muestra cantidad y progreso; búsqueda y filtros mantienen la puntuación y el estado de los grupos. Administración dispone de sugerencias de las diez categorías y mantiene los cambios sin guardar durante las actualizaciones.

Las categorías y postulados de las capturas son datos de prueba; siguen pendientes los 20 perfiles reales. El acceso conserva el código único solicitado: cinco jurados internos y cinco invitados. El código por sí solo no verifica identidad y los códigos administrativos del MD son conocidos. Para uso real aún se requiere servidor con HTTPS, almacenamiento persistente y controles adicionales de acceso.

Las pruebas de móvil, puntuación completa de 20 perfiles, agrupación, filtros y edición administrativa están en `tests/`. No se incluyen las bases de datos ni credenciales.
