import * as THREE from 'three';

export function setupLights(scene, preset = 'dia') {
  const presets = {
    dia: { key: 0xffddaa, fill: 0xaaccff },
    atardecer: { key: 0xff8844, fill: 0x4466aa }
  };

  const config = presets[preset];

  const keyLight = new THREE.DirectionalLight(config.key, 1.2);
  keyLight.position.set(10, 10, 10);

  const fillLight = new THREE.DirectionalLight(config.fill, 0.6);
  fillLight.position.set(-10, 5, 5);

  const rimLight = new THREE.DirectionalLight(0xffffff, 0.3);
  rimLight.position.set(0, 10, -10);

  const ambient = new THREE.AmbientLight(0x404040, 0.5);

  scene.add(keyLight, fillLight, rimLight, ambient);
}