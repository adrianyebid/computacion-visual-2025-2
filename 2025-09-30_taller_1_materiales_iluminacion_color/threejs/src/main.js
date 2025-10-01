import * as THREE from 'three';
import { loadModels } from './scene.js';
import { setupLights } from './lights.js';
import { createCameras } from './camera.js';
import { animateScene } from './animation.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

const scene = new THREE.Scene();
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Cámaras
const { perspective, ortho } = createCameras();
let activeCamera = perspective;

// OrbitControls (después de definir activeCamera)
const controls = new OrbitControls(activeCamera, renderer.domElement);
controls.target.set(0, 0, 0);
controls.update();

// Luces
setupLights(scene, 'dia'); // cambia en main.js para probar

// Modelos + animación (se ejecuta cuando los modelos están listos)
loadModels(scene, () => {
  animateScene(scene);
});

// Alternancia de cámara
document.addEventListener('keydown', (e) => {
  if (e.key === 'c') {
    activeCamera = activeCamera === perspective ? ortho : perspective;
    controls.object = activeCamera; // actualiza controles con nueva cámara
    controls.update();
  }
});

// Render loop
function render() {
  requestAnimationFrame(render);
  renderer.render(scene, activeCamera);
}
render();