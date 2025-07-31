'use client'

import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { CheckCircleIcon, ExclamationTriangleIcon, InformationCircleIcon, XCircleIcon, XMarkIcon } from '@heroicons/react/24/outline'
import { AlertCircle, Info, CheckCircle, X } from 'lucide-react'

interface ModernAlertProps {
  type?: 'success' | 'error' | 'warning' | 'info'
  title?: string
  message: string
  isVisible?: boolean
  onClose?: () => void
  autoClose?: boolean
  duration?: number
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'center'
  className?: string
}

export default function ModernAlert({
  type = 'info',
  title,
  message,
  isVisible = true,
  onClose,
  autoClose = false,
  duration = 5000,
  position = 'top-right',
  className = ''
}: ModernAlertProps) {
  const [visible, setVisible] = React.useState(isVisible)

  React.useEffect(() => {
    setVisible(isVisible)
  }, [isVisible])

  React.useEffect(() => {
    if (autoClose && visible) {
      const timer = setTimeout(() => {
        handleClose()
      }, duration)
      return () => clearTimeout(timer)
    }
  }, [autoClose, visible, duration])

  const handleClose = () => {
    setVisible(false)
    setTimeout(() => {
      onClose?.()
    }, 300)
  }

  const getTypeConfig = () => {
    switch (type) {
      case 'success':
        return {
          icon: CheckCircle,
          borderColor: 'border-emerald-400/50',
          iconColor: 'text-emerald-400',
          bgColor: 'bg-emerald-400/10',
          shadowColor: 'shadow-[0_0_20px_rgba(52,211,153,0.2)]'
        }
      case 'error':
        return {
          icon: AlertCircle,
          borderColor: 'border-red-400/50',
          iconColor: 'text-red-400',
          bgColor: 'bg-red-400/10',
          shadowColor: 'shadow-[0_0_20px_rgba(248,113,113,0.2)]'
        }
      case 'warning':
        return {
          icon: ExclamationTriangleIcon,
          borderColor: 'border-amber-400/50',
          iconColor: 'text-amber-400',
          bgColor: 'bg-amber-400/10',
          shadowColor: 'shadow-[0_0_20px_rgba(251,191,36,0.2)]'
        }
      default:
        return {
          icon: Info,
          borderColor: 'border-brand-400/50',
          iconColor: 'text-brand-400',
          bgColor: 'bg-brand-400/10',
          shadowColor: 'shadow-[0_0_20px_rgba(14,165,233,0.2)]'
        }
    }
  }

  const getPositionClasses = () => {
    switch (position) {
      case 'top-left':
        return 'top-6 left-6'
      case 'bottom-right':
        return 'bottom-6 right-6'
      case 'bottom-left':
        return 'bottom-6 left-6'
      case 'center':
        return 'top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2'
      default:
        return 'top-6 right-6'
    }
  }

  const typeConfig = getTypeConfig()
  const Icon = typeConfig.icon

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9, y: position.includes('bottom') ? 20 : -20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: position.includes('bottom') ? 20 : -20 }}
          transition={{ duration: 0.3, ease: "easeOut" }}
          className={`fixed z-[9999] max-w-md w-full ${getPositionClasses()} ${className}`}
        >
          <div className={`glass-card border-l-4 ${typeConfig.borderColor} ${typeConfig.shadowColor} relative overflow-hidden`}>
            {/* Background glow effect */}
            <div className={`absolute inset-0 ${typeConfig.bgColor} opacity-50`} />
            
            {/* Content */}
            <div className="relative flex items-start space-x-4 p-6">
              {/* Icon */}
              <div className="flex-shrink-0">
                <div className={`w-10 h-10 rounded-xl bg-gradient-to-br from-white/10 to-white/5 flex items-center justify-center ${typeConfig.shadowColor}`}>
                  <Icon className={`w-5 h-5 ${typeConfig.iconColor}`} />
                </div>
              </div>

              {/* Text Content */}
              <div className="flex-1 min-w-0">
                {title && (
                  <h3 className="text-lg font-semibold text-white mb-2">
                    {title}
                  </h3>
                )}
                <p className="text-sm text-white/80 leading-relaxed">
                  {message}
                </p>
              </div>

              {/* Close Button */}
              {onClose && (
                <motion.button
                  onClick={handleClose}
                  className="flex-shrink-0 w-8 h-8 glass rounded-lg flex items-center justify-center hover:shadow-neon transition-all duration-300 group"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <X className="w-4 h-4 text-white/60 group-hover:text-white" />
                </motion.button>
              )}
            </div>

            {/* Progress bar for auto-close */}
            {autoClose && (
              <motion.div
                className={`absolute bottom-0 left-0 h-1 ${typeConfig.borderColor.replace('border-', 'bg-').replace('/50', '')}`}
                initial={{ width: '100%' }}
                animate={{ width: '0%' }}
                transition={{ duration: duration / 1000, ease: "linear" }}
              />
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

// Toast-style notification hook
export function useModernToast() {
  const [alerts, setAlerts] = React.useState<Array<{
    id: string
    type: 'success' | 'error' | 'warning' | 'info'
    title?: string
    message: string
  }>>([])

  const addAlert = React.useCallback((alert: Omit<typeof alerts[0], 'id'>) => {
    const id = Math.random().toString(36).substr(2, 9)
    setAlerts(prev => [...prev, { ...alert, id }])
  }, [])

  const removeAlert = React.useCallback((id: string) => {
    setAlerts(prev => prev.filter(alert => alert.id !== id))
  }, [])

  const success = React.useCallback((message: string, title?: string) => {
    addAlert({ type: 'success', message, title })
  }, [addAlert])

  const error = React.useCallback((message: string, title?: string) => {
    addAlert({ type: 'error', message, title })
  }, [addAlert])

  const warning = React.useCallback((message: string, title?: string) => {
    addAlert({ type: 'warning', message, title })
  }, [addAlert])

  const info = React.useCallback((message: string, title?: string) => {
    addAlert({ type: 'info', message, title })
  }, [addAlert])

  const ToastContainer = React.useCallback(() => (
    <div className="fixed top-6 right-6 z-[9999] space-y-4 pointer-events-none">
      <AnimatePresence>
        {alerts.map((alert, index) => (
          <motion.div
            key={alert.id}
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 100 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className="pointer-events-auto"
          >
            <ModernAlert
              {...alert}
              onClose={() => removeAlert(alert.id)}
              autoClose
              duration={4000}
            />
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  ), [alerts, removeAlert])

  return {
    success,
    error,
    warning,
    info,
    ToastContainer
  }
}

// Inline alert component for forms and content
export function InlineAlert({
  type = 'info',
  message,
  className = ''
}: {
  type?: 'success' | 'error' | 'warning' | 'info'
  message: string
  className?: string
}) {
  const typeConfig = {
    success: {
      icon: CheckCircle,
      borderColor: 'border-emerald-400/40',
      iconColor: 'text-emerald-400',
      bgColor: 'bg-emerald-400/10'
    },
    error: {
      icon: AlertCircle,
      borderColor: 'border-red-400/40',
      iconColor: 'text-red-400',
      bgColor: 'bg-red-400/10'
    },
    warning: {
      icon: ExclamationTriangleIcon,
      borderColor: 'border-amber-400/40',
      iconColor: 'text-amber-400',
      bgColor: 'bg-amber-400/10'
    },
    info: {
      icon: Info,
      borderColor: 'border-brand-400/40',
      iconColor: 'text-brand-400',
      bgColor: 'bg-brand-400/10'
    }
  }[type]

  const Icon = typeConfig.icon

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`glass rounded-2xl p-4 border-l-4 ${typeConfig.borderColor} ${className}`}
    >
      <div className={`absolute inset-0 ${typeConfig.bgColor} rounded-2xl`} />
      <div className="relative flex items-center space-x-3">
        <Icon className={`w-5 h-5 ${typeConfig.iconColor} flex-shrink-0`} />
        <p className="text-sm text-white/80">{message}</p>
      </div>
    </motion.div>
  )
} 