'use client'

import React, { useState } from 'react'
import RepositoryAnalyzer from './components/RepositoryAnalyzer'

export default function HomePage() {
  const [showRepositoryAnalyzer, setShowRepositoryAnalyzer] = useState(false)

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
      color: 'white',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      {/* Navigation */}
      <nav style={{
        position: 'sticky',
        top: 0,
        zIndex: 50,
        backgroundColor: 'rgba(0, 0, 0, 0.3)',
        backdropFilter: 'blur(10px)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        padding: '1rem 0'
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
          padding: '0 1.5rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div style={{
              width: '40px',
              height: '40px',
              background: 'linear-gradient(45deg, #8b5cf6, #ec4899)',
              borderRadius: '12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '20px'
            }}>✨</div>
            <div>
              <h1 style={{
                fontSize: '1.5rem',
                fontWeight: 'bold',
                background: 'linear-gradient(45deg, #8b5cf6, #ec4899)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                margin: 0
              }}>AI-mVISE</h1>
              <p style={{
                fontSize: '0.75rem',
                color: '#9ca3af',
                margin: 0
              }}>Repository Intelligence</p>
            </div>
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <button style={{
              padding: '0.5rem 1rem',
              fontSize: '0.875rem',
              color: '#d1d5db',
              background: 'transparent',
              border: 'none',
              cursor: 'pointer',
              transition: 'color 0.2s'
            }}>Documentation</button>
            <button style={{
              padding: '0.5rem 1.5rem',
              background: 'linear-gradient(45deg, #8b5cf6, #ec4899)',
              borderRadius: '8px',
              color: 'white',
              fontWeight: '500',
              border: 'none',
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}>Get Started</button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section style={{ padding: '5rem 0' }}>
        <div style={{
          maxWidth: '1000px',
          margin: '0 auto',
          padding: '0 1.5rem',
          textAlign: 'center'
        }}>
          {/* Badge */}
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            background: 'rgba(255, 255, 255, 0.1)',
            backdropFilter: 'blur(10px)',
            borderRadius: '50px',
            padding: '0.5rem 1rem',
            marginBottom: '2rem',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            fontSize: '0.875rem'
          }}>
            <span style={{ color: '#fbbf24' }}>⭐</span>
            <span style={{ color: '#e5e7eb' }}>Powered by Claude AI</span>
            <div style={{
              width: '8px',
              height: '8px',
              background: '#10b981',
              borderRadius: '50%',
              animation: 'pulse 2s infinite'
            }}></div>
          </div>

          {/* Main Title */}
          <h1 style={{
            fontSize: 'clamp(3rem, 8vw, 5rem)',
            fontWeight: 'bold',
            marginBottom: '2rem',
            lineHeight: '1.1'
          }}>
            <div style={{
              background: 'linear-gradient(45deg, #8b5cf6, #ec4899, #06b6d4)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              marginBottom: '0.5rem'
            }}>AI-Powered</div>
            <div style={{ color: 'white' }}>Repository Intelligence</div>
          </h1>

          {/* Subtitle */}
          <p style={{
            fontSize: '1.25rem',
            color: '#d1d5db',
            marginBottom: '3rem',
            maxWidth: '600px',
            margin: '0 auto 3rem auto',
            lineHeight: '1.6'
          }}>
            Transform your codebase understanding with{' '}
            <span style={{
              background: 'linear-gradient(45deg, #8b5cf6, #ec4899)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              fontWeight: '600'
            }}>cutting-edge AI analysis</span>
            . Get comprehensive insights into quality, security, architecture, and team performance.
          </p>

          {/* CTA Buttons */}
          <div style={{
            display: 'flex',
            flexDirection: window.innerWidth < 640 ? 'column' : 'row',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '1rem',
            marginBottom: '4rem'
          }}>
            <button
              onClick={() => setShowRepositoryAnalyzer(true)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                padding: '1rem 2rem',
                background: 'linear-gradient(45deg, #8b5cf6, #ec4899)',
                borderRadius: '12px',
                color: 'white',
                fontWeight: '600',
                border: 'none',
                cursor: 'pointer',
                fontSize: '1.1rem',
                transition: 'all 0.2s',
                boxShadow: '0 10px 25px rgba(139, 92, 246, 0.3)'
              }}
                             onMouseOver={(e) => {
                 (e.target as HTMLElement).style.transform = 'scale(1.05)'
                 ;(e.target as HTMLElement).style.boxShadow = '0 15px 35px rgba(139, 92, 246, 0.4)'
               }}
               onMouseOut={(e) => {
                 (e.target as HTMLElement).style.transform = 'scale(1)'
                 ;(e.target as HTMLElement).style.boxShadow = '0 10px 25px rgba(139, 92, 246, 0.3)'
               }}
            >
              🔍 Analyze Repository →
            </button>

            <button style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
              padding: '1rem 2rem',
              background: 'rgba(255, 255, 255, 0.1)',
              backdropFilter: 'blur(10px)',
              borderRadius: '12px',
              color: 'white',
              fontWeight: '600',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              cursor: 'pointer',
              fontSize: '1.1rem',
              transition: 'all 0.2s'
            }}>
              ▶️ Watch Demo
              <div style={{
                width: '8px',
                height: '8px',
                background: '#ef4444',
                borderRadius: '50%',
                animation: 'pulse 2s infinite'
              }}></div>
            </button>
          </div>

          {/* Platform Support */}
          <div style={{
            background: 'rgba(255, 255, 255, 0.05)',
            backdropFilter: 'blur(10px)',
            borderRadius: '16px',
            padding: '1.5rem',
            maxWidth: '500px',
            margin: '0 auto',
            border: '1px solid rgba(255, 255, 255, 0.1)'
          }}>
            <p style={{
              color: '#9ca3af',
              fontSize: '0.875rem',
              marginBottom: '1rem'
            }}>Supports all major platforms</p>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '2rem'
            }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                color: '#d1d5db',
                cursor: 'pointer',
                transition: 'color 0.2s'
              }}>
                <span style={{ fontSize: '1.5rem' }}>🐙</span>
                <span style={{ fontWeight: '500' }}>GitHub</span>
              </div>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                color: '#d1d5db',
                cursor: 'pointer',
                transition: 'color 0.2s'
              }}>
                <span style={{ fontSize: '1.5rem' }}>🦊</span>
                <span style={{ fontWeight: '500' }}>GitLab</span>
              </div>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                color: '#d1d5db',
                cursor: 'pointer',
                transition: 'color 0.2s'
              }}>
                <span style={{ fontSize: '1.5rem' }}>🪣</span>
                <span style={{ fontWeight: '500' }}>Bitbucket</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section style={{
        padding: '4rem 0',
        background: 'rgba(0, 0, 0, 0.2)'
      }}>
        <div style={{
          maxWidth: '1000px',
          margin: '0 auto',
          padding: '0 1.5rem'
        }}>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '1.5rem'
          }}>
            {[
              { value: "2.8K+", label: "Repositories Analyzed" },
              { value: "18.4K+", label: "Issues Resolved" },
              { value: "99.9%", label: "Accuracy Rate" },
              { value: "< 15min", label: "Analysis Time" }
            ].map((stat, index) => (
              <div key={stat.label} style={{
                textAlign: 'center',
                padding: '1.5rem',
                background: 'rgba(255, 255, 255, 0.05)',
                backdropFilter: 'blur(10px)',
                borderRadius: '12px',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                transition: 'all 0.2s'
              }}>
                <div style={{
                  fontSize: '2rem',
                  fontWeight: 'bold',
                  background: 'linear-gradient(45deg, #8b5cf6, #ec4899)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  marginBottom: '0.5rem'
                }}>{stat.value}</div>
                <div style={{
                  color: '#9ca3af',
                  fontSize: '0.875rem'
                }}>{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section style={{ padding: '5rem 0' }}>
        <div style={{
          maxWidth: '1000px',
          margin: '0 auto',
          padding: '0 1.5rem'
        }}>
          <div style={{
            textAlign: 'center',
            marginBottom: '4rem'
          }}>
            <h2 style={{
              fontSize: 'clamp(2.5rem, 6vw, 4rem)',
              fontWeight: 'bold',
              marginBottom: '1.5rem'
            }}>
              <div style={{
                background: 'linear-gradient(45deg, #8b5cf6, #ec4899)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent'
              }}>Comprehensive</div>
              <div style={{ color: 'white' }}>Analysis Suite</div>
            </h2>
            <p style={{
              fontSize: '1.25rem',
              color: '#d1d5db',
              maxWidth: '600px',
              margin: '0 auto'
            }}>
              Every aspect of your codebase, analyzed with cutting-edge AI
            </p>
          </div>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: '2rem'
          }}>
            {[
              {
                title: "🧠 Code Intelligence",
                description: "AI-powered analysis of complexity, quality, and maintainability patterns"
              },
              {
                title: "🛡️ Security Scanning",
                description: "Advanced vulnerability detection and security threat analysis"
              },
              {
                title: "📦 Dependency Health",
                description: "Monitor outdated packages, licenses, and vulnerability risks"
              },
              {
                title: "⚡ Performance Insights",
                description: "Identify bottlenecks and optimization opportunities"
              },
              {
                title: "🤖 AI Recommendations",
                description: "Intelligent modernization roadmaps and best practices"
              },
              {
                title: "📊 Quality Metrics",
                description: "Industry-standard scoring with actionable improvement plans"
              }
            ].map((feature, index) => (
              <div key={feature.title} style={{
                background: 'rgba(255, 255, 255, 0.05)',
                backdropFilter: 'blur(10px)',
                borderRadius: '12px',
                padding: '1.5rem',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                transition: 'all 0.3s'
              }}
                             onMouseOver={(e) => {
                 (e.target as HTMLElement).style.background = 'rgba(255, 255, 255, 0.1)'
                 ;(e.target as HTMLElement).style.transform = 'translateY(-5px)'
               }}
               onMouseOut={(e) => {
                 (e.target as HTMLElement).style.background = 'rgba(255, 255, 255, 0.05)'
                 ;(e.target as HTMLElement).style.transform = 'translateY(0)'
               }}
              >
                <h3 style={{
                  fontSize: '1.25rem',
                  fontWeight: 'bold',
                  marginBottom: '0.75rem',
                  color: 'white'
                }}>{feature.title}</h3>
                <p style={{
                  color: '#d1d5db',
                  lineHeight: '1.6'
                }}>{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section style={{
        padding: '5rem 0',
        background: 'rgba(0, 0, 0, 0.2)'
      }}>
        <div style={{
          maxWidth: '800px',
          margin: '0 auto',
          padding: '0 1.5rem',
          textAlign: 'center'
        }}>
          <div style={{
            background: 'rgba(255, 255, 255, 0.05)',
            backdropFilter: 'blur(10px)',
            borderRadius: '16px',
            padding: '3rem',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            position: 'relative',
            overflow: 'hidden'
          }}>
            <div style={{
              position: 'absolute',
              inset: 0,
              background: 'linear-gradient(45deg, rgba(139, 92, 246, 0.1), rgba(236, 72, 153, 0.1))'
            }}></div>
            <div style={{ position: 'relative', zIndex: 10 }}>
              <div style={{
                fontSize: '4rem',
                marginBottom: '1.5rem'
              }}>🚀</div>
              <h2 style={{
                fontSize: 'clamp(2rem, 5vw, 3rem)',
                fontWeight: 'bold',
                marginBottom: '1.5rem',
                background: 'linear-gradient(45deg, #8b5cf6, #ec4899)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent'
              }}>
                Ready to revolutionize your code analysis?
              </h2>
              <p style={{
                fontSize: '1.25rem',
                color: '#d1d5db',
                marginBottom: '2rem',
                maxWidth: '500px',
                margin: '0 auto 2rem auto'
              }}>
                Join thousands of developers who trust AI-mVISE for comprehensive repository insights
              </p>
              <button
                onClick={() => setShowRepositoryAnalyzer(true)}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.75rem',
                  padding: '1.25rem 3rem',
                  background: 'linear-gradient(45deg, #8b5cf6, #ec4899)',
                  borderRadius: '12px',
                  color: 'white',
                  fontWeight: '600',
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: '1.25rem',
                  transition: 'all 0.2s',
                  boxShadow: '0 15px 35px rgba(139, 92, 246, 0.4)'
                }}
                                 onMouseOver={(e) => {
                   (e.target as HTMLElement).style.transform = 'scale(1.05)'
                   ;(e.target as HTMLElement).style.boxShadow = '0 20px 45px rgba(139, 92, 246, 0.5)'
                 }}
                 onMouseOut={(e) => {
                   (e.target as HTMLElement).style.transform = 'scale(1)'
                   ;(e.target as HTMLElement).style.boxShadow = '0 15px 35px rgba(139, 92, 246, 0.4)'
                 }}
              >
                🚀 Start Analyzing Now ✨
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{
        borderTop: '1px solid rgba(255, 255, 255, 0.1)',
        padding: '4rem 0'
      }}>
        <div style={{
          maxWidth: '1000px',
          margin: '0 auto',
          padding: '0 1.5rem'
        }}>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
            gap: '2rem'
          }}>
            <div>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                marginBottom: '1.5rem'
              }}>
                <div style={{
                  width: '40px',
                  height: '40px',
                  background: 'linear-gradient(45deg, #8b5cf6, #ec4899)',
                  borderRadius: '12px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '20px'
                }}>✨</div>
                <span style={{
                  fontSize: '1.75rem',
                  fontWeight: 'bold',
                  background: 'linear-gradient(45deg, #8b5cf6, #ec4899)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent'
                }}>AI-mVISE</span>
              </div>
              <p style={{
                color: '#9ca3af',
                maxWidth: '300px',
                marginBottom: '1.5rem'
              }}>
                Empowering development teams worldwide with AI-driven insights to build exceptional software.
              </p>
            </div>
            
            <div>
              <h3 style={{
                fontWeight: '600',
                color: 'white',
                marginBottom: '1rem'
              }}>Product</h3>
              <ul style={{
                listStyle: 'none',
                padding: 0,
                margin: 0
              }}>
                {["Features", "Pricing", "API", "Integrations"].map((link) => (
                  <li key={link} style={{ marginBottom: '0.5rem' }}>
                    <a href="#" style={{
                      color: '#9ca3af',
                      textDecoration: 'none',
                      transition: 'color 0.2s'
                    }}>{link}</a>
                  </li>
                ))}
              </ul>
            </div>
            
            <div>
              <h3 style={{
                fontWeight: '600',
                color: 'white',
                marginBottom: '1rem'
              }}>Resources</h3>
              <ul style={{
                listStyle: 'none',
                padding: 0,
                margin: 0
              }}>
                {["Documentation", "Blog", "Community", "Support"].map((link) => (
                  <li key={link} style={{ marginBottom: '0.5rem' }}>
                    <a href="#" style={{
                      color: '#9ca3af',
                      textDecoration: 'none',
                      transition: 'color 0.2s'
                    }}>{link}</a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          
          <div style={{
            borderTop: '1px solid rgba(255, 255, 255, 0.1)',
            marginTop: '3rem',
            paddingTop: '2rem',
            textAlign: 'center'
          }}>
            <p style={{ color: '#9ca3af' }}>
              © 2024 mVISE AG. Built with{' '}
              <span style={{ color: '#ef4444' }}>♥</span>{' '}
              for developers worldwide.
            </p>
          </div>
        </div>
      </footer>

      {/* Repository Analyzer Modal */}
      {showRepositoryAnalyzer && (
        <div style={{
          position: 'fixed',
          inset: 0,
          zIndex: 999,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'rgba(0, 0, 0, 0.6)',
          backdropFilter: 'blur(5px)',
          padding: '1rem'
        }}>
          <div style={{
            width: '100%',
            maxWidth: '1000px'
          }}>
            <RepositoryAnalyzer onClose={() => setShowRepositoryAnalyzer(false)} />
          </div>
        </div>
      )}

      <style jsx>{`
        @keyframes pulse {
          0%, 100% {
            opacity: 1;
          }
          50% {
            opacity: .5;
          }
        }
      `}</style>
    </div>
  )
} 