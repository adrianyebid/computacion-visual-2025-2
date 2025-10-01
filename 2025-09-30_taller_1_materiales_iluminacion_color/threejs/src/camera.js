import * as THREE from 'three';

export function createCameras() {
  const aspect = window.innerWidth / window.innerHeight;

  const perspective = new THREE.PerspectiveCamera(75, aspect, 0.1, 100);
  perspective.position.set(0, 10, 20);

  const orthoSize = 5;
  const ortho = new THREE.OrthographicCamera(
    -orthoSize * aspect,
    orthoSize * aspect,
    orthoSize,
    -orthoSize,
    0.1,
    100
  );
  ortho.position.set(0, 10, 20);

  return { perspective, ortho };
}