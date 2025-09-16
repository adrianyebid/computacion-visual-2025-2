import { useState } from 'react'
import { Canvas } from '@react-three/fiber'
import Box from './Box'
import './App.css'
import { OrbitControls } from '@react-three/drei'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className="app-container">
        <Canvas 
          shadows 
          style={{ background: "#87CEEB" }}
          camera={{ position: [0, 0, 5], fov: 50 }}
        >

          <OrbitControls 
          enablePan={true}    // Permite desplazar
          enableZoom={true}   // Permite zoom
          enableRotate={true} // Permite rotar
        />

          {/* Luces */}
          <ambientLight intensity={0.5} />
          <directionalLight
            castShadow
            position={[10, 10, 10]}
            shadow-mapSize={[2048, 2048]}
          />
          <pointLight position={[10, 10, 10]} />

          <Box/> 
        </Canvas>
      </div>
    </>
  )
}

export default App