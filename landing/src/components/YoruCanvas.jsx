import React, { Suspense, useState, useEffect } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import { YoruCharacter } from './Yoru3DMascot'

/**
 * Loading Spinner Fallback untuk 3D Canvas
 */
function CanvasLoader() {
  return (
    <div className="flex flex-col items-center justify-center h-full w-full">
      <div className="w-12 h-12 border-3 border-yoru-border border-t-yoru-gold rounded-full animate-spin mb-3"></div>
      <span className="text-xs text-yoru-gold/80 font-medium tracking-wider uppercase">
        Memanggil Yoru…
      </span>
    </div>
  )
}

/**
 * 2D Fallback Karakter untuk perangkat low-end / tanpa WebGL
 */
function Fallback2DYoru({ isHovered }) {
  return (
    <div className="flex flex-col items-center justify-center h-full w-full select-none">
      <div className={`relative w-48 h-48 rounded-full bg-gradient-to-b from-[#1A2133] to-[#0F1422] border-2 border-yoru-gold/40 flex items-center justify-center transition-transform duration-500 animate-float-slow ${isHovered ? 'scale-105' : ''}`}>
        <div className="absolute inset-0 rounded-full border border-yoru-gold/20 animate-ping opacity-25"></div>
        <div className="w-28 h-28 rounded-full bg-[#0A0C13] flex items-center justify-center gap-6 shadow-inner">
          <div className="w-3.5 h-6 rounded-full bg-yoru-gold animate-pulse"></div>
          <div className="w-3.5 h-6 rounded-full bg-yoru-gold animate-pulse"></div>
        </div>
        <span className="absolute -top-3 text-2xl">⭐</span>
      </div>
      <span className="mt-4 text-xs text-yoru-muted font-medium">Mode Hemat Daya (2D Fallback)</span>
    </div>
  )
}

/**
 * YoruCanvas Container dengan deteksi WebGL & optimasi mobile
 */
export default function YoruCanvas({ isHovered = false, className = '' }) {
  const [canRender3D, setCanRender3D] = useState(true)

  useEffect(() => {
    // Deteksi WebGL dan perangkat low-end
    try {
      const canvas = document.createElement('canvas')
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl')
      const isLowEnd = navigator.hardwareConcurrency && navigator.hardwareConcurrency < 2
      if (!gl || isLowEnd) {
        setCanRender3D(false)
      }
    } catch (e) {
      setCanRender3D(false)
    }
  }, [])

  if (!canRender3D) {
    return (
      <div className={`w-full h-[400px] sm:h-[480px] ${className}`}>
        <Fallback2DYoru isHovered={isHovered} />
      </div>
    )
  }

  return (
    <div className={`w-full h-[400px] sm:h-[480px] relative ${className}`}>
      <Suspense fallback={<CanvasLoader />}>
        <Canvas
          camera={{ position: [0, 0, 3.2], fov: 45 }}
          dpr={[1, 2]} // Optimasi resolusi layar retina
          gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
        >
          {/* Pencahayaan Lembut Nuansa Malam */}
          <ambientLight intensity={0.65} color="#D8E2FD" />
          <directionalLight position={[3, 4, 2]} intensity={1.2} color="#FCE7B2" />
          <directionalLight position={[-3, -2, -1]} intensity={0.4} color="#60A5FA" />

          {/* Maskot Yoru */}
          <YoruCharacter isHovered={isHovered} />

          {/* Orbit Controls dibatasi agar interaksi tetap intuitif */}
          <OrbitControls
            enableZoom={false}
            enablePan={false}
            maxPolarAngle={Math.PI / 1.7}
            minPolarAngle={Math.PI / 2.4}
            maxAzimuthAngle={Math.PI / 3.5}
            minAzimuthAngle={-Math.PI / 3.5}
          />
        </Canvas>
      </Suspense>
    </div>
  )
}
