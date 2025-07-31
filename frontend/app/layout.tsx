import React from 'react'
import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from './providers'
import { Toaster } from 'react-hot-toast'
import ScrollToTop from './components/ScrollToTop'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  viewportFit: 'cover',
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#0ea5e9' },
    { media: '(prefers-color-scheme: dark)', color: '#0ea5e9' },
  ],
  colorScheme: 'dark light',
}

export const metadata: Metadata = {
  title: {
    default: 'AI-mVISE Repository Analyzer | Intelligent Code Analysis',
    template: '%s | AI-mVISE'
  },
  description: 'Revolutionary AI-powered repository analysis platform. Get comprehensive insights into code quality, security vulnerabilities, architecture patterns, and team performance with cutting-edge artificial intelligence.',
  keywords: [
    'AI code analysis',
    'repository analyzer', 
    'code quality',
    'security scanning',
    'AI-powered development',
    'software engineering tools',
    'mVISE',
    'intelligent code review',
    'automated testing',
    'dependency analysis'
  ],
  authors: [{ name: 'mVISE AG', url: 'https://mvise.de' }],
  creator: 'mVISE AG',
  publisher: 'mVISE AG',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://ai-mvise.com'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: 'AI-mVISE Repository Analyzer | Intelligent Code Analysis',
    description: 'Revolutionary AI-powered repository analysis platform for comprehensive code insights.',
    url: 'https://ai-mvise.com',
    siteName: 'AI-mVISE',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'AI-mVISE Repository Analyzer',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'AI-mVISE Repository Analyzer',
    description: 'Revolutionary AI-powered repository analysis platform for comprehensive code insights.',
    images: ['/twitter-image.jpg'],
    creator: '@mVISE_AG',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  manifest: '/manifest.json',
  icons: {
    icon: [
      { url: '/favicon-16x16.png', sizes: '16x16', type: 'image/png' },
      { url: '/favicon-32x32.png', sizes: '32x32', type: 'image/png' },
    ],
    apple: [
      { url: '/apple-touch-icon.png', sizes: '180x180', type: 'image/png' },
    ],
    other: [
      {
        rel: 'mask-icon',
        url: '/safari-pinned-tab.svg',
        color: '#0ea5e9',
      },
    ],
  },
  verification: {
    google: 'your-google-site-verification',
    yandex: 'your-yandex-verification',
  },
  category: 'technology',
  classification: 'AI-powered developer tools',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'black-translucent',
    title: 'AI-mVISE',
    startupImage: [
      {
        url: '/apple-startup-1125x2436.png',
        media: '(device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3)',
      },
    ],
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} h-full scroll-smooth`} suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link rel="dns-prefetch" href="//fonts.googleapis.com" />
        <link rel="dns-prefetch" href="//fonts.gstatic.com" />
        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
        <meta name="apple-mobile-web-app-title" content="AI-mVISE" />
        <meta name="application-name" content="AI-mVISE" />
        <meta name="msapplication-TileColor" content="#0ea5e9" />
        <meta name="msapplication-config" content="/browserconfig.xml" />
      </head>
      <body className={`${inter.className} h-full bg-gradient-to-br from-slate-900 via-purple-900/20 to-slate-900 text-white antialiased select-brand overflow-x-hidden`}>
        <Providers>
          {/* Background Effects */}
          <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
            <div className="absolute inset-0 bg-dot-pattern opacity-10"></div>
            <div className="absolute top-0 left-1/4 w-96 h-96 bg-gradient-cosmic rounded-full blur-3xl opacity-20 animate-float"></div>
            <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-gradient-sunset rounded-full blur-3xl opacity-15 animate-blob"></div>
            <div className="absolute top-1/3 right-1/3 w-60 h-60 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full blur-3xl opacity-10 animate-pulse"></div>
          </div>

          {/* Main Content */}
          <div className="relative z-10 min-h-full">
            <main className="min-h-screen">
              {children}
            </main>
          </div>

          {/* Toast Notifications */}
          <Toaster
            position="top-right"
            gutter={12}
            containerClassName="!z-[9999]"
            toastOptions={{
              duration: 5000,
              className: 'glass-card !bg-slate-800/90 !backdrop-blur-xl !border-white/20 !text-white',
              style: {
                background: 'rgba(30, 41, 59, 0.9)',
                backdropFilter: 'blur(16px)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                borderRadius: '1rem',
                color: '#ffffff',
                boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37), 0 0 20px rgba(14, 165, 233, 0.2)',
                fontSize: '14px',
                fontWeight: '500',
                maxWidth: '400px',
              },
              success: {
                className: '!border-emerald-400/40',
                style: {
                  borderColor: 'rgba(52, 211, 153, 0.4)',
                  boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37), 0 0 20px rgba(52, 211, 153, 0.3)',
                },
                iconTheme: {
                  primary: '#10b981',
                  secondary: '#ffffff',
                },
              },
              error: {
                className: '!border-red-400/40',
                style: {
                  borderColor: 'rgba(248, 113, 113, 0.4)',
                  boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37), 0 0 20px rgba(248, 113, 113, 0.3)',
                },
                iconTheme: {
                  primary: '#ef4444',
                  secondary: '#ffffff',
                },
              },
              loading: {
                className: '!border-brand-400/40',
                style: {
                  borderColor: 'rgba(14, 165, 233, 0.4)',
                  boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37), 0 0 20px rgba(14, 165, 233, 0.3)',
                },
                iconTheme: {
                  primary: '#0ea5e9',
                  secondary: '#ffffff',
                },
              },
            }}
          />

          {/* Scroll to Top Button - Now as Client Component */}
          <ScrollToTop />
        </Providers>
      </body>
    </html>
  )
} 