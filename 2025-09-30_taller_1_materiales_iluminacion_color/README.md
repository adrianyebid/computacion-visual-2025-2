# Taller 1: Materiales, Iluminación y Shaders en Three.js

Este proyecto presenta una escena 3D interactiva construida con **Three.js**, enfocada en la implementación técnica de materiales PBR, esquemas de iluminación cinematográfica, shaders procedurales personalizados con GLSL y animaciones mediante GSAP.

## 1. Breve explicación del mundo creado
La escena es una composición abstracta de "naturaleza muerta digital" que contrasta elementos arquitectónicos, orgánicos y cotidianos sobre un suelo matemático. La idea principal es explorar cómo la luz interactúa de forma distinta sobre superficies texturizadas (modelos PBR) frente a superficies puramente algorítmicas (shaders procedurales), permitiendo al usuario manipular la percepción del espacio mediante cambios de cámara e iluminación.

## 2. Modelos GLB usados
Los modelos fueron importados usando `GLTFLoader`. Se les aplicó un material unificado para estudiar el comportamiento de la luz sobre distintas topologías.

| Objeto | Archivo Fuente | Modificaciones (Transformaciones) |
| :--- | :--- | :--- |
| **Organic** | `organic.glb` | **Escala:** 10.0 <br> **Posición:** (30, 1, 0) <br> **Rotación:** Animada en eje Y. |
| **Building** | `building.glb` | **Escala:** 3.0 <br> **Posición:** (-40, 0, 0) |
| **Table** | `table.glb` | **Escala:** 1.2 <br> **Posición:** (0, 0, 0) <br> **Animación:** Levitación en Y. |

## 3. Iluminación
Se implementó un esquema de **Iluminación de Tres Puntos** para dar volumen y realismo, complementado con luz ambiental.

### Esquema aplicado (Luces):
1.  **Key Light (Principal):** `DirectionalLight` (Intensidad 1.2). Posición `(10, 10, 10)`. Proyecta las sombras principales.
2.  **Fill Light (Relleno):** `DirectionalLight` (Intensidad 0.6). Posición `(-10, 5, 5)`. Suaviza las áreas oscuras.
3.  **Rim Light (Contraluz):** `DirectionalLight` (Intensidad 0.3). Posición `(0, 10, -10)`. Separa los objetos del fondo.
4.  **Ambient:** `AmbientLight` (Intensidad 0.5). Base gris neutra `0x404040`.

### Presets de Iluminación:
El sistema permite cambiar entre ambientes definidos por temperatura de color:
* **Día:** Key cálido (`0xffddaa`) vs Fill frío (`0xaaccff`).
* **Atardecer:** Key naranja fuerte (`0xff8844`) vs Fill azul profundo (`0x4466aa`).

## 4. Materiales y Texturas (PBR)
Se utilizó `THREE.MeshStandardMaterial` para lograr un renderizado basado en física (Physically Based Rendering).

* **Parámetros:**
    * **Metalness:** `0.2`. Se definió un valor bajo para simular materiales mayormente dieléctricos con un ligero brillo especular.
* **Mapas de Textura:**
    * `map`: Color base.
    * `roughnessMap`: Define la micro-superficie (mate vs brillante).
    * `normalMap`: Añade detalle de relieve geométrico sin aumentar polígonos.
* **Justificación:** El uso de PBR asegura la conservación de la energía lumínica, haciendo que los materiales reaccionen de manera coherente al cambiar los presets de luz (Día/Atardecer).

## 5. Shaders Procedurales
Se implementaron dos `ShaderMaterial` escritos en GLSL para los planos del suelo, evitando el uso de imágenes externas.

1.  **Damero (Checker):**
    * **Ubicación:** Plano en Z = 20.
    * **Lógica:** Usa `step(0.5, fract(vUv * 10.0))` en ambos ejes (X e Y) y calcula la diferencia absoluta `abs(cx - cy)` para alternar colores blanco y negro.
2.  **Bandas Verticales (Stripes):**
    * **Ubicación:** Plano en Z = -20.
    * **Lógica:** Usa `step(0.5, fract(vUv.x * 20.0))` solo en el eje X para crear franjas azules y blancas.

## 6. Cámaras
El proyecto permite alternar vistas con la tecla **'C'**:

* **Perspectiva (`PerspectiveCamera`):** FOV 75. Imita el ojo humano con puntos de fuga. Usada para inmersión y apreciación de profundidad.
* **Ortográfica (`OrthographicCamera`):** Tamaño de vista 5. Elimina la deformación de profundidad. Usada para analizar proporciones técnicas y alineación de los objetos sin distorsión.

## 7. Animaciones
Implementadas con la librería **GSAP** para suavizado (tweening):

* **Objeto Organic:** Rotación continua en el eje Y (`Math.PI * 2`) con repetición infinita.
* **Objeto Table:** Movimiento de "yoyo" (subir y bajar) en posición Y hasta 0.5.
* **Luz Principal:** La luz direccional se mueve en el eje X (hasta 5), lo que provoca que las sombras de la escena se desplacen dinámicamente en tiempo real.

## 8. Modelo de Color
Se trabajó en espacio **RGB** hexadecimal.
* **Contraste Perceptual:** Se aplicó la teoría de colores complementarios (Naranja/Azul) en la iluminación.
* **Justificación:** Al usar una Key Light cálida y una Fill Light fría, se maximiza el contraste cromático en las sombras, lo que ayuda al cerebro a interpretar mejor el volumen tridimensional (similar a la percepción CIELAB donde los canales a* y b* oponen estos tonos).

---

## Galería de Resultados

### Capturas de Pantalla de la Escena
![Vista General](https://github.com/adrianyebid/computacion-visual-2025-2/blob/master/2025-09-30_taller_1_materiales_iluminacion_color/renders/Screenshot%202025-09-30%20203253.png?raw=true)

![Detalle Materiales](https://github.com/adrianyebid/computacion-visual-2025-2/blob/master/2025-09-30_taller_1_materiales_iluminacion_color/renders/Screenshot%202025-09-30%20203445.png?raw=true)

![Iluminacion 1](https://github.com/adrianyebid/computacion-visual-2025-2/blob/master/2025-09-30_taller_1_materiales_iluminacion_color/renders/Screenshot%202025-09-30%20203454.png?raw=true)

![Iluminacion 2](https://github.com/adrianyebid/computacion-visual-2025-2/blob/master/2025-09-30_taller_1_materiales_iluminacion_color/renders/Screenshot%202025-09-30%20203504.png?raw=true)

![Perspectiva vs Ortho](https://github.com/adrianyebid/computacion-visual-2025-2/blob/master/2025-09-30_taller_1_materiales_iluminacion_color/renders/Screenshot%202025-09-30%20203531.png?raw=true)

![Shader Detail](https://github.com/adrianyebid/computacion-visual-2025-2/blob/master/2025-09-30_taller_1_materiales_iluminacion_color/renders/Screenshot%202025-09-30%20203556.png?raw=true)

### Demostración (GIFs)

**1. Alternancia de Cámaras (Perspectiva / Ortográfica)**
![Camera Switch](https://github.com/adrianyebid/computacion-visual-2025-2/blob/master/2025-09-30_taller_1_materiales_iluminacion_color/renders/gif-camera.gif?raw=true)

**2. Shaders Procedurales en acción**
![Shaders](https://github.com/adrianyebid/computacion-visual-2025-2/blob/master/2025-09-30_taller_1_materiales_iluminacion_color/renders/gif-shaders.gif?raw=true)

**3. Animaciones y Movimiento de Luces**
![Animations](https://github.com/adrianyebid/computacion-visual-2025-2/blob/master/2025-09-30_taller_1_materiales_iluminacion_color/renders/git-animations.gif?raw=true)
