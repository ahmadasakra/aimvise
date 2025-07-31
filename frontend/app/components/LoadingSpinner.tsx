'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Sparkles, Code2, Brain } from 'lucide-react'

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl'
  variant?: 'primary' | 'cosmic' | 'minimal'
  message?: string
  className?: string
}

export default function LoadingSpinner({ 
  size = 'md', 
  variant = 'primary',
  message,
  className = '' 
}: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8', 
    lg: 'w-12 h-12',
    xl: 'w-16 h-16'
  }

  const iconSizes = {
    sm: 'w-2 h-2',
    md: 'w-4 h-4',
    lg: 'w-6 h-6', 
    xl: 'w-8 h-8'
  }

  if (variant === 'cosmic') {
    return (
      <div className={`flex flex-col items-center justify-center space-y-4 ${className}`}>
        <div className="relative">
          {/* Outer rotating ring */}
          <motion.div
            className={`${sizeClasses[size]} rounded-full border-2 border-transparent bg-gradient-cosmic`}
            animate={{ rotate: 360 }}
            transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
            style={{
              background: 'conic-gradient(from 0deg, #8b5cf6, #ec4899, #06b6d4, #8b5cf6)',
              mask: 'radial-gradient(farthest-side, transparent calc(100% - 2px), black calc(100% - 2px))',
              WebkitMask: 'radial-gradient(farthest-side, transparent calc(100% - 2px), black calc(100% - 2px))'
            }}
          />
          
          {/* Inner pulsing core */}
          <motion.div
            className={`absolute inset-2 bg-gradient-cosmic rounded-full flex items-center justify-center`}
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <Brain className={`${iconSizes[size]} text-white`} />
          </motion.div>
          
          {/* Glow effect */}
          <div className={`absolute inset-0 ${sizeClasses[size]} rounded-full bg-gradient-cosmic blur-md opacity-40 animate-pulse`} />
        </div>
        
        {message && (
          <motion.p 
            className="text-sm text-white/70 animate-pulse"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            {message}
          </motion.p>
        )}
      </div>
    )
  }

  if (variant === 'minimal') {
    return (
      <div className={`flex items-center justify-center space-x-1 ${className}`}>
        {[0, 1, 2].map((i) => (
          <motion.div
            key={i}
            className="w-2 h-2 bg-brand-400 rounded-full"
            animate={{
              scale: [1, 1.5, 1],
              opacity: [0.5, 1, 0.5],
            }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              delay: i * 0.2,
            }}
          />
        ))}
        {message && <span className="ml-3 text-sm text-white/70">{message}</span>}
      </div>
    )
  }

  // Primary variant (default)
  return (
    <div className={`flex flex-col items-center justify-center space-y-3 ${className}`}>
      <div className="relative">
        {/* Main spinner */}
        <motion.div
          className={`${sizeClasses[size]} rounded-full border-2 border-brand-400/20 border-t-brand-400`}
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        />
        
        {/* Inner decorative elements */}
        <motion.div
          className="absolute inset-2 flex items-center justify-center"
          animate={{ rotate: -360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
        >
          <Sparkles className={`${iconSizes[size]} text-brand-400 opacity-60`} />
        </motion.div>
        
        {/* Outer glow */}
        <div className={`absolute inset-0 ${sizeClasses[size]} rounded-full bg-brand-400 blur-md opacity-20 animate-pulse`} />
      </div>
      
      {message && (
        <motion.p 
          className="text-sm text-white/70 text-center max-w-xs"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          {message}
        </motion.p>
      )}
    </div>
  )
}

// Skeleton loader for content
export function SkeletonLoader({ className = '' }: { className?: string }) {
  return (
    <div className={`animate-pulse ${className}`}>
      <div className="glass rounded-2xl p-6 space-y-4">
        <div className="h-4 bg-gradient-to-r from-white/10 to-white/5 rounded-full w-3/4"></div>
        <div className="space-y-2">
          <div className="h-3 bg-gradient-to-r from-white/10 to-white/5 rounded-full"></div>
          <div className="h-3 bg-gradient-to-r from-white/5 to-white/10 rounded-full w-5/6"></div>
        </div>
        <div className="h-8 bg-gradient-to-r from-white/5 to-white/10 rounded-xl w-1/2"></div>
      </div>
    </div>
  )
}

// Full page loading overlay
export function LoadingOverlay({ message }: { message?: string }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[9999] backdrop-blur-xl bg-slate-900/60 flex items-center justify-center p-4"
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="glass-card p-8 text-center max-w-sm w-full"
      >
        <LoadingSpinner size="xl" variant="cosmic" message={message} />
      </motion.div>
    </motion.div>
  )
} 