**1. Explain the difference between working on a branch and working directly on main. Why is it recommended to always use branches in collaborative projects? \[1 pts]**



**Answer:** Trabajar en el main significa modificar directamente la versión principal del proyecto, lo que puede poner en riesgo el código principal si se introducen errores (mas aún en trabajos colaborativos). En cambio, trabajar en una branch permite desarrollar nuevas funciones o corregir errores de forma aislada al código principal, sin afectar el proyecto antes de que los cambios sean validados. En proyectos colaborativos se recomienda usar branches porque ayudan a evitar afectar la versión principal del proyecto con errores, permiten que varias personas trabajen diferentes tareas en paralelo y facilitan la revisión antes de integrar los cambios.





**5. Create a Pull Request (PR) on GitHub to merge the group branch into main. Explain in which cases a reviewer might reject the PR (e.g., code conflicts, formatting errors, failure to follow instructions, etc.).**



**Answer:** Un Pull Request se utiliza para proponer cambios desde una branch hacia main, pero un revisor puede rechazarlo en los siguientes casos:



* Conflictos de código: el revisor rechaza el PR porque los cambios de la rama chocan con modificaciones que ya existen en main, lo que impide que Git-Hub fusione automáticamente los cambios; y, por consiguiente, se podrían generar errores en el proyecto.



* Errores o fallos: el revisor rechaza el PR porque el nuevo código rompe funcionalidades existentes o contiene bugs, lo que pondría en riesgo la estabilidad del proyecto principal.



* Problemas de formato o estilo: el revisor rechaza el PR porque no se siguen las guías de estilo del proyecto (p.e. nombres de variables), lo que afecta la consistencia y dificulta el mantenimiento del código.



* Implementación incompleta: el revisor rechaza el PR porque la funcionalidad o corrección está a medias o no cumple con los requisitos, y main debe recibir únicamente código terminado.



* Incumplimiento de instrucciones del proyecto: el revisor rechaza el PR porque no se documentaron los cambios, no se incluyeron pruebas o no se respetaron las convenciones de trabajo, lo que afecta el orden y la trazabilidad del proyecto.
