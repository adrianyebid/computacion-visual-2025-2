import { useRef } from "react"
import { useFrame } from "@react-three/fiber"


export default function Box() {  
    const boxRef = useRef();
  
  useFrame((state) => {
    const time = state.clock.elapsedTime
    boxRef.current.rotation.y += 0.01
    boxRef.current.position.x = Math.sin(time) * 2
    const scale = Math.sin(time) * 0.3 + 1 
    boxRef.current.scale.set(scale, scale, scale)
  })

  return (
    <mesh ref={boxRef}>
      <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="hotpink"/>
    </mesh>
  )
}