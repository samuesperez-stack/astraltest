# Panel TOYP · acceso del MD

[Proyecto actualizado](TOYP_Panel_Proyecto_V3.zip?raw=true) · [Vista móvil](TOYP_Acceso_Un_Codigo.png) · [Código fuente](../../../projects/toyp-votacion/)

Acceso por código único, como en el MD: cinco internos JUR-INT-01 a 05, cinco invitados JUR-INV-01 a 05, y los dos códigos administrativos originales. Los códigos se asocian a las cuentas internas existentes y sus votos.

**Riesgo:** un código conocido permite suplantar a ese jurado o a administración. HTTPS no autentica a la persona; controla el acceso a la red y la distribución de códigos. Los códigos administrativos del ejemplo son conocidos. La versión anterior con contraseña se conserva en el historial de Git.

Pruebas con diez jurados, segunda vuelta, reconexión, bloqueo y conflicto entre dispositivos. Siguen pendientes los 20 postulados reales y el despliegue en un servidor persistente con HTTPS. La base de datos y las contraseñas previas no se incluyen en el ZIP.
