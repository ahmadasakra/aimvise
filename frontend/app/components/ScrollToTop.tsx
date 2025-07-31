'use client'

import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ArrowUpIcon } from '@heroicons/react/24/outline'

export default function ScrollToTop() {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const toggleVisibility = () => {
      if (window.pageYOffset > 300) {
        setIsVisible(true)
      } else {
        setIsVisible(false)
      }
    }

    window.addEventListener('scroll', toggleVisibility)
    return () => window.removeEventListener('scroll', toggleVisibility)
  }, [])

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    })
  }

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.button
          onClick={scrollToTop}
          className="fixed bottom-8 right-8 z-50 w-12 h-12 glass rounded-2xl flex items-center justify-center hover:shadow-neon hover:scale-110 transition-all duration-300 group"
          aria-label="Scroll to top"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.8 }}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
        >
          <ArrowUpIcon className="w-5 h-5 text-white group-hover:text-brand-300 transition-colors" />
          
          {/* Glow effect */}
          <div className="absolute inset-0 w-12 h-12 bg-brand-400 rounded-2xl blur-md opacity-0 group-hover:opacity-30 transition-opacity duration-300" />
        </motion.button>
      )}
    </AnimatePresence>
  )
} 