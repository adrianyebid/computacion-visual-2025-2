# 🧪 Jerarquías y Transformaciones: El Árbol del Movimiento

## 🧩 Ejercicio Realizado

**Breve explicación (qué hice y por qué):**  
En este ejercicio implementé una escena 3D interactiva usando **React Three Fiber** y **Vite**, enfocándome en comprender cómo funcionan las **transformaciones jerárquicas** en un entorno tridimensional.  

Construí una estructura con tres niveles (padre, hijo y nieto) para observar cómo las transformaciones —traslación, rotación y escala— se propagan en cascada a los objetos hijos.  
El objetivo fue visualizar de forma práctica cómo un cambio en el objeto padre afecta automáticamente a toda la jerarquía, lo que representa un principio clave en los sistemas de gráficos 3D.

También incorporé **controles interactivos con Leva** para manipular el nodo padre en tiempo real (posición, rotación y escala), permitiendo experimentar directamente con las transformaciones y su efecto en los objetos anidados.  

Finalmente, añadí **ayudas visuales** como ejes y grillas para facilitar la comprensión espacial y la relación entre los diferentes niveles de la jerarquía.

# 👁️ Visión Artificial con OpenCV

## 🧩 Ejercicio Realizado

**Breve explicación (qué hice y por qué):**  
En este ejercicio exploré los fundamentos de la **visión artificial** utilizando la biblioteca **OpenCV en Python**. El objetivo fue entender cómo los computadores pueden procesar imágenes digitales mediante operaciones matemáticas básicas aplicadas sobre los píxeles.

Apliqué **filtros convolucionales** (como desenfoque, enfoque y detección de bordes) para observar cómo modifican las características visuales de una imagen. Utilicé operadores como **Sobel**, **Laplaciano** y **Canny** para comparar sus resultados y comprender cómo cada uno detecta los contornos desde distintos enfoques.

El ejercicio me permitió visualizar de manera práctica la relación entre las **operaciones matemáticas y los efectos visuales**, entendiendo cómo estas transformaciones sirven como base para tareas más avanzadas como la segmentación y el reconocimiento de objetos. Elegí este ejercicio porque proporciona una base sólida para comprender el procesamiento de imágenes antes de pasar a técnicas más complejas basadas en redes neuronales.

# 🎨 Rasterización desde Cero (Línea, Círculo, Triángulo)

## 🧩 Ejercicio Realizado  

**Breve explicación (qué hice y por qué):**  
En este ejercicio implementé desde cero los **algoritmos clásicos de rasterización** para generar primitivas gráficas básicas —líneas, círculos y triángulos— sin utilizar librerías de alto nivel.  

Desarrollé el **algoritmo de Bresenham** para trazar líneas píxel a píxel con máxima eficiencia entera, el **algoritmo del punto medio** para dibujar círculos aprovechando su simetría, y el método **scanline** para el **relleno de triángulos**. Estas implementaciones las realicé en **Python**, apoyándome únicamente en **Pillow, NumPy y Matplotlib** para la visualización final.  

El objetivo principal fue comprender cómo los gráficos vectoriales se transforman en píxeles (rasterización) y cómo la precisión y eficiencia de cada algoritmo afectan el resultado visual.  
Elegí este ejercicio porque permite **entender los fundamentos matemáticos detrás del renderizado digital**, sentando las bases para procesos más avanzados como el shading o la proyección en 3D.

---

# 📐 Análisis Geométrico (Centroide, Área, Perímetro)

## 🧩 Ejercicio Realizado  

**Breve explicación (qué hice y por qué):**  
En este ejercicio apliqué técnicas de **análisis geométrico** sobre imágenes binarizadas utilizando **OpenCV**. Mi objetivo fue extraer métricas descriptivas de los contornos —como **área**, **perímetro** y **centroide**— para comprender cómo los algoritmos de visión artificial cuantifican la forma de los objetos.  

Utilicé funciones como `findContours`, `contourArea`, `arcLength` y los **momentos geométricos** para calcular los centroides. Luego, **etiqueté visualmente** cada objeto con sus métricas sobre la imagen y generé un **GIF animado** mostrando los resultados. Como extensión, añadí una **clasificación automática básica** (triángulo, cuadrado o círculo) mediante aproximación de contornos.  

Elegí este ejercicio porque demuestra cómo a partir de simples contornos se pueden **obtener propiedades cuantitativas y cualitativas de las figuras**, un paso esencial en la **extracción de características** y en sistemas de reconocimiento de formas.
