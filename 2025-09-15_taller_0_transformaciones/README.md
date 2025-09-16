# Transformaciones en Computación Visual

Este repositorio contiene tres implementaciones distintas de transformaciones geométricas aplicadas a figuras (triángulos y cubos) en diferentes entornos de programación.

---

### Breve explicación
Se implementa un **triángulo 2D** al que se aplican transformaciones geométricas usando **multiplicación de matrices** con `numpy` y visualización con `matplotlib`.  
Las transformaciones realizadas son:
- **Traslación**
- **Rotación**
- **Escalado**


Se implementa un **cubo 3D** en una escena de **React Three Fiber** que:
- Rota sobre su eje.
- Se traslada siguiendo una trayectoria senoidal.
- Cambia de tamaño con una función dependiente del tiempo.

La escena además puede explorarse con controles de cámara (rotar, trasladar y hacer zoom).


El archivo principal de la animación está en:  
[`Box.jsx`](./threejs/src/Box.jsx)

---

Se implementa un **cubo 3D** en Processing que:
- Rota sobre su propio eje.
- Se traslada en trayectoria senoidal.
- Escala dinámicamente con una función temporal.

