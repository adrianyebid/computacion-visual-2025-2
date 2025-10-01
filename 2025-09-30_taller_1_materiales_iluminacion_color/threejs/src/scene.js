import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

export function loadModels(scene, onComplete) {
  const loader = new GLTFLoader();
  const textureLoader = new THREE.TextureLoader();

  // Material PBR con texturas reales
  const pbrMaterial = new THREE.MeshStandardMaterial({
    map: textureLoader.load('/textures/color.jpg'),
    roughnessMap: textureLoader.load('/textures/roughness.jpg'),
    normalMap: textureLoader.load('/textures/normalGL.jpg'),
    metalness: 0.2
  });

  const models = [
    { name: 'organic', file: 'organic.glb', position: [30, 1, 0], scale: 10.0 },
    { name: 'building', file: 'building.glb', position: [-40, 0, 0], scale: 3.0 },
    { name: 'table', file: 'table.glb', position: [0, 0, 0], scale: 1.2 },
  ];

  let loadedCount = 0;

  models.forEach(({ name, file, position, scale }) => {
    loader.load(`/models/${file}`, (gltf) => {
      const model = gltf.scene;
      model.name = name;
      model.position.set(...position);
      model.scale.set(scale, scale, scale);

      model.traverse((child) => {
        if (child.isMesh) {
          child.material = pbrMaterial;
        }
      });

      scene.add(model);
      console.log(`${name} size:`, new THREE.Box3().setFromObject(model).getSize(new THREE.Vector3()));

      loadedCount++;
      if (loadedCount === models.length && typeof onComplete === 'function') {
        onComplete();
      }
    });
  });

  // Plano con shader damero
  const checkerMaterial = new THREE.ShaderMaterial({
    vertexShader: `
      varying vec2 vUv;
      void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      varying vec2 vUv;
      void main() {
        float cx = step(0.5, fract(vUv.x * 10.0));
        float cy = step(0.5, fract(vUv.y * 10.0));
        float checker = abs(cx - cy);
        vec3 color = mix(vec3(1.0), vec3(0.0), checker);
        gl_FragColor = vec4(color, 1.0);
      }
    `
  });
  const checkerPlane = new THREE.Mesh(new THREE.PlaneGeometry(10, 10), checkerMaterial);
  checkerPlane.rotation.x = -Math.PI / 2;
  checkerPlane.position.set(0, 0.01, 20);
  scene.add(checkerPlane);

  // Plano con shader de bandas verticales
  const stripeMaterial = new THREE.ShaderMaterial({
    vertexShader: `
      varying vec2 vUv;
      void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      varying vec2 vUv;
      void main() {
        float stripe = step(0.5, fract(vUv.x * 20.0));
        vec3 color = mix(vec3(0.2, 0.6, 1.0), vec3(1.0), stripe);
        gl_FragColor = vec4(color, 1.0);
      }
    `
  });
  const stripePlane = new THREE.Mesh(new THREE.PlaneGeometry(10, 10), stripeMaterial);
  stripePlane.rotation.x = -Math.PI / 2;
  stripePlane.position.set(0, 0.01, -20);
  scene.add(stripePlane);
}