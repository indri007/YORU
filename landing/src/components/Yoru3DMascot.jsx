import React, { useRef, useState, useEffect, useMemo } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { Float, Sparkles, MeshDistortMaterial } from '@react-three/drei'
import * as THREE from 'three'

/**
 * Yoru3DMascot Component
 * Karakter AI Assistant 3D: "Yoru" - The Cute Night Guardian
 * Dibuat murni dari primitive shapes Three.js (Sphere, Capsule, Torus)
 * Bebas hak cipta, ramah, kawaii cute-robot dengan tema malam & bintang.
 * 
 * Fitur Animasi:
 * 1. Idle/Floating: Gerakan mengambang sinusoidal + rotasi lembut
 * 2. Greeting: Melambai satu tangan saat pertama kali dimuat
 * 3. Interactive Hover/Click: Menoleh mengikuti kursor + aura emas menyala
 */

export function YoruCharacter({ state = 'idle', isHovered = false }) {
  const groupRef = useRef()
  const headRef = useRef()
  const rightHandRef = useRef()
  const leftHandRef = useRef()
  const eyeLeftRef = useRef()
  const eyeRightRef = useRef()
  const haloRef = useRef()
  const lightRef = useRef()

  // State untuk greeting animation (one-shot saat pertama load)
  const [greetingProgress, setGreetingProgress] = useState(0)
  const [isBlinking, setIsBlinking] = useState(false)

  // Timer kedipan mata otomatis (random interval)
  useEffect(() => {
    const blinkInterval = setInterval(() => {
      setIsBlinking(true)
      setTimeout(() => setIsBlinking(false), 180)
    }, 3800 + Math.random() * 2000)
    return () => clearInterval(blinkInterval)
  }, [])

  // Mouse tracking menggunakan koordinat normalisasi Three.js
  const { mouse } = useThree()

  useFrame((stateContext, delta) => {
    const time = stateContext.clock.getElapsedTime()

    // 1. ANIMASI IDLE / FLOATING (Sinusoidal float + slight tilt)
    if (groupRef.current) {
      // Floating naik-turun halus
      groupRef.current.position.y = Math.sin(time * 1.8) * 0.12
      // Rotasi lembut di sumbu Z
      groupRef.current.rotation.z = Math.sin(time * 0.9) * 0.04
    }

    // 2. MOUSE TRACKING (Kepala menoleh halus mengikuti kursor)
    if (headRef.current) {
      const targetRotX = -mouse.y * 0.35
      const targetRotY = mouse.x * 0.45
      headRef.current.rotation.x = THREE.MathUtils.lerp(headRef.current.rotation.x, targetRotX, delta * 3)
      headRef.current.rotation.y = THREE.MathUtils.lerp(headRef.current.rotation.y, targetRotY, delta * 3)
    }

    // 3. ANIMASI GREETING (Melambai saat pertama load)
    if (greetingProgress < 1) {
      setGreetingProgress((prev) => Math.min(prev + delta * 0.8, 1))
      if (rightHandRef.current) {
        // Angkat tangan kanan dan lambaikan cepat
        const wave = Math.sin(time * 8) * 0.3
        rightHandRef.current.position.y = 0.6 + wave
        rightHandRef.current.position.x = 0.75
        rightHandRef.current.position.z = 0.25
      }
    } else {
      // Kembali ke gerakan mengambang tangan normal
      if (rightHandRef.current) {
        rightHandRef.current.position.y = THREE.MathUtils.lerp(
          rightHandRef.current.position.y,
          -0.1 + Math.sin(time * 2.2 + 1) * 0.08,
          delta * 4
        )
        rightHandRef.current.position.x = THREE.MathUtils.lerp(
          rightHandRef.current.position.x,
          isHovered ? 0.75 : 0.68,
          delta * 4
        )
      }
    }

    // Tangan kiri mengambang santai
    if (leftHandRef.current) {
      leftHandRef.current.position.y = -0.1 + Math.sin(time * 2.2) * 0.08
      leftHandRef.current.position.x = isHovered ? -0.75 : -0.68
    }

    // 4. ROTASI HALO / RING PENJAGA
    if (haloRef.current) {
      haloRef.current.rotation.z += delta * 0.4
      haloRef.current.rotation.x = Math.PI / 2.3 + Math.sin(time) * 0.08
    }

    // 5. INTERACTIVE HOVER REACTION (Aura emas memancar lebih terang)
    if (lightRef.current) {
      const targetIntensity = isHovered ? 3.5 : 1.8
      lightRef.current.intensity = THREE.MathUtils.lerp(lightRef.current.intensity, targetIntensity, delta * 5)
    }

    // 6. BLINK LOGIC (Mata menyipit/berkedip)
    const eyeScaleY = isBlinking ? 0.1 : 1
    if (eyeLeftRef.current && eyeRightRef.current) {
      eyeLeftRef.current.scale.y = eyeScaleY
      eyeRightRef.current.scale.y = eyeScaleY
    }
  })

  // Material Palette (Dark Navy, Metallic Charcoal, Warm Gold Emissive)
  const bodyMaterial = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: '#131722',
        roughness: 0.25,
        metalness: 0.5,
      }),
    []
  )

  const bellyMaterial = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: '#1A2133',
        roughness: 0.4,
        metalness: 0.2,
      }),
    []
  )

  const goldGlowMaterial = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: '#E8B64C',
        emissive: '#E8B64C',
        emissiveIntensity: isHovered ? 1.8 : 1.1,
        roughness: 0.2,
      }),
    [isHovered]
  )

  const eyeMaterial = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: '#FDFCF7',
        emissive: isHovered ? '#FDE047' : '#E8B64C',
        emissiveIntensity: 2.2,
        roughness: 0.1,
      }),
    [isHovered]
  )

  return (
    <group ref={groupRef} position={[0, -0.2, 0]}>
      {/* Cahaya Titik Emas Penjaga (Glow Aura) */}
      <pointLight ref={lightRef} position={[0, 0.4, 0.9]} color="#E8B64C" distance={4} intensity={2} />

      {/* Partikel Bintang Mengambang di Sekitar Yoru */}
      <Sparkles count={45} scale={2.8} size={2.5} speed={0.4} color="#E8B64C" opacity={0.6} />

      {/* ================================================================== */}
      {/* 1. BADAN UTAMA (Cute Rounded Torso) */}
      {/* ================================================================== */}
      <mesh position={[0, -0.3, 0]} material={bodyMaterial}>
        {/* Bentuk capsule chubby low-poly halus */}
        <sphereGeometry args={[0.55, 32, 32]} />
      </mesh>

      {/* Perut / Pelindung Dada (Belly Accent) */}
      <mesh position={[0, -0.26, 0.2]} material={bellyMaterial}>
        <sphereGeometry args={[0.42, 24, 24]} />
      </mesh>

      {/* Bintang Penjaga di Dada (Glowing Heart Emblem) */}
      <mesh position={[0, -0.22, 0.52]} material={goldGlowMaterial}>
        <octahedronGeometry args={[0.09, 0]} />
      </mesh>

      {/* ================================================================== */}
      {/* 2. KEPALA DENGAN MOUSE TRACKING (Head & Face) */}
      {/* ================================================================== */}
      <group ref={headRef} position={[0, 0.38, 0]}>
        {/* Batok Kepala Bulat Kawaii */}
        <mesh material={bodyMaterial}>
          <sphereGeometry args={[0.48, 32, 32]} />
        </mesh>

        {/* Visor Muka Gelap Kaca (Cute Screen Face) */}
        <mesh position={[0, -0.02, 0.22]} rotation={[-0.05, 0, 0]}>
          <sphereGeometry args={[0.38, 32, 24]} />
          <meshStandardMaterial color="#0A0C13" roughness={0.15} metalness={0.8} />
        </mesh>

        {/* MATA KIRI (Glowing Eye Left) */}
        <mesh ref={eyeLeftRef} position={[-0.15, 0.02, 0.52]} material={eyeMaterial}>
          <capsuleGeometry args={[0.045, 0.07, 16, 16]} />
        </mesh>

        {/* MATA KANAN (Glowing Eye Right) */}
        <mesh ref={eyeRightRef} position={[0.15, 0.02, 0.52]} material={eyeMaterial}>
          <capsuleGeometry args={[0.045, 0.07, 16, 16]} />
        </mesh>

        {/* Senyum Kecil / Cute Blush Accent */}
        <mesh position={[-0.22, -0.1, 0.46]} material={goldGlowMaterial}>
          <sphereGeometry args={[0.035, 12, 12]} />
        </mesh>
        <mesh position={[0.22, -0.1, 0.46]} material={goldGlowMaterial}>
          <sphereGeometry args={[0.035, 12, 12]} />
        </mesh>

        {/* ANTENA BINTANG / TELINGA PENJAGA (Night Guardian Ears) */}
        <group position={[-0.32, 0.36, 0]} rotation={[0, 0, 0.4]}>
          <mesh material={bodyMaterial}>
            <coneGeometry args={[0.1, 0.28, 16]} />
          </mesh>
          <mesh position={[0, 0.17, 0]} material={goldGlowMaterial}>
            <sphereGeometry args={[0.055, 12, 12]} />
          </mesh>
        </group>

        <group position={[0.32, 0.36, 0]} rotation={[0, 0, -0.4]}>
          <mesh material={bodyMaterial}>
            <coneGeometry args={[0.1, 0.28, 16]} />
          </mesh>
          <mesh position={[0, 0.17, 0]} material={goldGlowMaterial}>
            <sphereGeometry args={[0.055, 12, 12]} />
          </mesh>
        </group>
      </group>

      {/* ================================================================== */}
      {/* 3. TANGAN ORB MENGAMBANG (Floating Orb Hands) */}
      {/* ================================================================== */}
      <mesh ref={leftHandRef} position={[-0.68, -0.1, 0]} material={bodyMaterial}>
        <sphereGeometry args={[0.14, 20, 20]} />
      </mesh>

      <mesh ref={rightHandRef} position={[0.68, -0.1, 0]} material={bodyMaterial}>
        <sphereGeometry args={[0.14, 20, 20]} />
      </mesh>

      {/* ================================================================== */}
      {/* 4. HALO PENJAGA MALAM (Night Guardian Orbit Halo) */}
      {/* ================================================================== */}
      <group ref={haloRef} position={[0, 0.45, 0]}>
        <mesh material={goldGlowMaterial}>
          <torusGeometry args={[0.62, 0.018, 16, 64]} />
        </mesh>
        {/* Satelit Bintang Kecil yang Mengorbit */}
        <mesh position={[0.62, 0, 0]} material={goldGlowMaterial}>
          <octahedronGeometry args={[0.045, 0]} />
        </mesh>
      </group>

      {/* Kaki / Penyangga Pijakan Levitasi */}
      <mesh position={[-0.2, -0.75, 0]} material={bodyMaterial}>
        <capsuleGeometry args={[0.09, 0.18, 16, 16]} />
      </mesh>
      <mesh position={[0.2, -0.75, 0]} material={bodyMaterial}>
        <capsuleGeometry args={[0.09, 0.18, 16, 16]} />
      </mesh>
    </group>
  )
}
