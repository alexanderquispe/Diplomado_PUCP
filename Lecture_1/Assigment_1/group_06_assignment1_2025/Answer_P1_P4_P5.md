**1. Explain the difference between working on a branch and working directly on main. Why is it recommended to always use branches in collaborative projects? \[1 pts]**



**Answer:** 



Trabajar en el main significa modificar directamente la versión principal del proyecto, lo que puede poner en riesgo el código principal si se introducen errores (mas aún en trabajos colaborativos). En cambio, trabajar en una branch permite desarrollar nuevas funciones o corregir errores de forma aislada al código principal, sin afectar el proyecto antes de que los cambios sean validados. En proyectos colaborativos se recomienda usar branches porque ayudan a evitar afectar la versión principal del proyecto con errores, permiten que varias personas trabajen diferentes tareas en paralelo y facilitan la revisión antes de integrar los cambios.


Working on main means directly modifying the main version of the project, wich can put the main code at risk if bugs are introduced (even more so in collaborative projects). Working on a branch, on the other hand, allows you to develop new features oor fix bugs in isolation from the main code, without affecting the project before the changes are validated. In collaborative projects, using branches is recommended because they help avoid affecting the main version of the project with bugs, allow multiple people to work on different tasks in parallel, and facilitate review before integrating changes.



**3. Make a commit with the following message: Added my favorite movies. Write down the corresponding Git command.**

**Choose one group member to act as the repository maintainer.**



Git command: 

* git add Lecture\_1/Assigment\_1/group\_06\_assignment1\_2025/movies.md
* git commit -m "#1700 Added my favourite movies"



Repository maintainer: Nicole Molina



**5. Create a Pull Request (PR) on GitHub to merge the group branch into main. Explain in which cases a reviewer might reject the PR (e.g., code conflicts, formatting errors, failure to follow instructions, etc.).**



**Answer:** 
Un Pull Request se utiliza para proponer cambios desde una branch hacia main, pero un revisor puede rechazarlo en los siguientes casos:



* Conflictos de código: el revisor rechaza el PR porque los cambios de la rama chocan con modificaciones que ya existen en main, lo que impide que Git-Hub fusione automáticamente los cambios; y, por consiguiente, se podrían generar errores en el proyecto.



* Errores o fallos: el revisor rechaza el PR porque el nuevo código rompe funcionalidades existentes o contiene bugs, lo que pondría en riesgo la estabilidad del proyecto principal.



* Problemas de formato o estilo: el revisor rechaza el PR porque no se siguen las guías de estilo del proyecto (p.e. nombres de variables), lo que afecta la consistencia y dificulta el mantenimiento del código.



* Implementación incompleta: el revisor rechaza el PR porque la funcionalidad o corrección está a medias o no cumple con los requisitos, y main debe recibir únicamente código terminado.



* Incumplimiento de instrucciones del proyecto: el revisor rechaza el PR porque no se documentaron los cambios, no se incluyeron pruebas o no se respetaron las convenciones de trabajo, lo que afecta el orden y la trazabilidad del proyecto.



A Pull Request is used to propose changes from a branch to main, but a reviewer can reject it in the following cases:



* Code conflicts: The reviewer rejects the PR because the branch's changes conflict with existing changes in main, preventing GitHub from automatically merging the changes and, consequently, potentially creating errors in the project.



* Bugs or errors: The reviewer rejects the PR because the new code breaks existing functionality or contains bugs, which would jeopardize the stability of the main project.



* Formatting or style issues: The reviewer rejects the PR because it doesn't follow the project's style guidelines (e.g., variable names), which affects consistency and makes the code difficult to maintain.



* Incomplete implementation: The reviewer rejects the PR because the functionality or fix is ​​unfinished or doesn't meet requirements, and main should receive only completed code.



* Failure to comply with project instructions: The reviewer rejects the PR because changes were not documented, tests were not included, or work conventions were not respected, which affects the order and traceability of the project.
