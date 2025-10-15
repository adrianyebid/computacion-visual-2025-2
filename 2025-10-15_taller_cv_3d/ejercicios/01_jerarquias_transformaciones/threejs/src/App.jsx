import { useState, useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Stats } from '@react-three/drei'
import { Leva, useControls } from 'leva'
import './App.css'

// Componente Nieto - tercer nivel de la jerarquía
function Nieto({ position, color }) {
  return (
    <mesh position={position}>
      <dodecahedronGeometry args={[0.5, 0]} />
      <meshStandardMaterial color={color} />
    </mesh>
  )
}

// Componente Hijo - segundo nivel de la jerarquía
function Hijo({ position, rotation, color }) {
  return (
    <group position={position} rotation={rotation}>
      <mesh>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color={color} />
      </mesh>
      
      {/* Nietos - posicionados relativos al hijo */}
      <Nieto position={[0, 1.5, 0]} color="pink" />
      <Nieto position={[1.5, 0, 0]} color="lightblue" />
    </group>
  )
}

// Componente Padre - primer nivel de la jerarquía
function Padre() {
  const groupRef = useRef()
  
  // Controles para transformaciones del padre usando Leva
  const { 
    rotationSpeed, 
    positionX, 
    positionY,
    scale
  } = useControls('Padre', {
    rotationSpeed: { value: 0.5, min: 0, max: 5, step: 0.1 },
    positionX: { value: 0, min: -5, max: 5, step: 0.1 },
    positionY: { value: 0, min: -5, max: 5, step: 0.1 },
    scale: { value: 1, min: 0.5, max: 2, step: 0.1 }
  })

  // Animación - el padre rota según el control rotationSpeed
  useFrame((state, delta) => {
    if (groupRef.current) {
      groupRef.current.rotation.y += delta * rotationSpeed
    }
  })

  return (
    <group 
      ref={groupRef} 
      position={[positionX, positionY, 0]}
      scale={scale}
    >
      {/* Objeto del padre */}
      <mesh>
        <torusGeometry args={[2, 0.5, 16, 32]} />
        <meshStandardMaterial color="orange" />
      </mesh>
      
      {/* Hijos - posicionados relativos al padre */}
      <Hijo 
        position={[0, 0, 3]} 
        rotation={[0, Math.PI / 4, 0]} 
        color="green" 
      />
      <Hijo 
        position={[3, 0, 0]} 
        rotation={[0, -Math.PI / 4, 0]} 
        color="blue" 
      />
    </group>
  )
}

function Scene() {
  return (
    <>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
      <Padre />
      <OrbitControls />
      <Stats />
      <axesHelper scale={10} />
      <gridHelper />
    </>
  )
}

function App() {
  return (
    <div className="app">
      <Leva collapsed />
      <div className="info-panel">
        <h1>Sistema Jerárquico 3D</h1>
        <p>Demonstración de transformaciones en cascada padre-hijo-nieto</p>
        <div className="legend">
          <div><span className="color-box orange"></span> Padre (Toro)</div>
          <div><span className="color-box green"></span><span className="color-box blue"></span> Hijos (Cubos)</div>
          <div><span className="color-box pink"></span><span className="color-box lightblue"></span> Nietos (Dodecaedros)</div>
        </div>
        <p>Usa los controles en el panel para modificar el nodo padre y ver cómo afecta a toda la jerarquía.</p>
      </div>
      <Canvas camera={{ position: [0, 5, 10], fov: 50 }}>
        <Scene />
      </Canvas>
    </div>
  )
}

export default App