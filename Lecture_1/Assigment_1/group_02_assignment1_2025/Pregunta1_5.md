# Pregunta 1: Diferencia entre trabajar en rama vs main

Trabajar directamente en la rama main significa que todos los cambios se realizan inmediatamente en la versión principal del proyecto, lo cual presenta varios riesgos significativos. Cuando múltiples desarrolladores modifican main simultáneamente, se pueden generar conflictos y errores que afecten la estabilidad del código base. Además, cualquier error introducido impacta inmediatamente la versión "oficial" del proyecto, sin posibilidad de revisión previa. 

Por el contrario, trabajar en una rama permite crear una copia independiente del código donde se pueden realizar cambios de forma aislada. Esto permite experimentar y desarrollar nuevas características sin comprometer el código principal. Los cambios permanecen separados hasta que estén completamente listos y hayan sido probados adecuadamente.

En proyectos colaborativos, el uso de ramas es fundamental por varias razones críticas. Primero, proporciona seguridad al mantener main en un estado funcional en todo momento. Segundo, facilita la organización, permitiendo que cada desarrollador o equipo trabaje en características específicas de manera independiente. Tercero, habilita un proceso de revisión, donde los cambios pueden ser evaluados antes de su integración. Finalmente, mejora la colaboración al evitar conflictos entre desarrolladores y proporcionar un historial trazable de todos los cambios realizados en el proyecto.

# Pregunta 5: Casos donde un revisor rechazaría un Pull Request

Un revisor puede rechazar un Pull Request por problemas que comprometen la calidad y funcionalidad del código, especialmente cuando existen conflictos de merge que impiden la fusión automática con la rama. Estos conflictos surgen cuando los mismos archivos han sido modificados de manera incompatible en diferentes ramas. Asimismo, código que contiene errores en la codificación o sintaxis hasta que estos problemas sean resueltos.

El incumplimiento de las instrucciones específicas del proyecto es una causa frecuente de rechazo que refleja falta de atención a los detalles. Esto incluye contenido faltante como no proporcionar, por ejemplo, las tres películas requeridas, información incompleta donde falten elementos como título, año o sinopsis, usar nombres de archivo incorrectos diferentes a movies.md, o emplear mensajes de commit que no coincidan exactamente con lo solicitado, como "Añadí mis películas favoritas".
