import gsap from 'gsap';

export function animateScene(scene) {
  const organic = scene.getObjectByName('organic');
  const table = scene.getObjectByName('table');
  const light = scene.children.find(obj => obj.isDirectionalLight);

  if (organic) {
    gsap.to(organic.rotation, { y: Math.PI * 2, duration: 5, repeat: -1 });
  }

  if (table) {
    gsap.to(table.position, { y: 0.5, duration: 2, yoyo: true, repeat: -1 });
  }

  if (light) {
    gsap.to(light.position, { x: 5, duration: 3, yoyo: true, repeat: -1 });
  }
}