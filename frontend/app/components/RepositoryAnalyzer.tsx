'use client'

import React, { useState, useEffect } from 'react'
import DetailedReport from './DetailedReport'

interface RepositoryAnalyzerProps {
  onClose: () => void
}

interface AnalysisResult {
  id: string
  repository_url: string
  repository_name: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  overall_scores?: {
    overall_quality_score: number
    architecture_score: number
    security_score: number
    maintainability_score: number
  }
  repository_overview?: {
    languages: string[]
    lines_of_code: number
    total_files: number
  }
  ai_insights?: {
    architecture_pattern: string
    strengths: string[]
    weaknesses: string[]
    recommendations: string[]
  }
  technical_metrics?: {
    security_vulnerabilities: number
    dependencies_outdated: number
  }
  executive_summary?: string
  business_impact?: {
    technical_debt_hours: number
    development_velocity: string
  }
  investment_recommendations?: Array<{
    priority: number
    task: string
    effort_hours: number
    business_value: string
  }>
}

export default function RepositoryAnalyzer({ onClose }: RepositoryAnalyzerProps) {
  const [repositoryUrl, setRepositoryUrl] = useState('')
  const [githubToken, setGithubToken] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState('')
  const [progress, setProgress] = useState(0)
  const [currentStage, setCurrentStage] = useState('')
  const [analysisId, setAnalysisId] = useState('')
  const [showDetailedReport, setShowDetailedReport] = useState(false)

  // Poll for progress updates
  useEffect(() => {
    if (!analysisId || !isAnalyzing) return

    const pollProgress = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/analysis/${analysisId}/progress`)
        if (!response.ok) throw new Error('Failed to get progress')
        
        const data = await response.json()
        setProgress(data.progress_percentage || 0)
        setCurrentStage(data.current_stage || '')
        
        if (data.status === 'completed') {
          // Get final results
          const resultResponse = await fetch(`http://localhost:8000/api/analysis/${analysisId}`)
          if (resultResponse.ok) {
            const result = await resultResponse.json()
            setAnalysisResult(result)
            setIsAnalyzing(false)
          }
        } else if (data.status === 'failed') {
          setError('Analysis failed. Please try again.')
          setIsAnalyzing(false)
        }
      } catch (err) {
        console.error('Progress polling error:', err)
      }
    }

    const interval = setInterval(pollProgress, 2000)
    return () => clearInterval(interval)
  }, [analysisId, isAnalyzing])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!repositoryUrl.trim()) {
      setError('Please enter a repository URL')
      return
    }

    setIsAnalyzing(true)
    setError('')
    setProgress(0)
    setCurrentStage('Starting analysis...')

    try {
      // Start analysis
      const response = await fetch('http://localhost:8000/api/analysis/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          repository_url: repositoryUrl, 
          github_token: githubToken || undefined, 
          analysis_type: 'comprehensive' 
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to start analysis')
      }

      const result = await response.json()
      setAnalysisId(result.analysis_id)
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed')
      setIsAnalyzing(false)
    }
  }

  // Single comprehensive analysis type
  const analysisInfo = {
    title: 'Deep AI Analysis',
    description: 'Comprehensive AI-powered analysis with Amazon Bedrock Claude',
    duration: '~15-30 minutes',
    features: [
      'Architecture & Design Patterns Analysis',
      'Technology Stack Assessment', 
      'Code Quality & Maintainability',
      'Security Vulnerability Scan',
      'Business Impact Analysis',
      'Investment Recommendations',
      'Technical Debt Assessment',
      'Team & Process Insights'
    ]
  }

  const getQualityColor = (score: number) => {
    if (score >= 90) return '#10b981' // green
    if (score >= 80) return '#f59e0b' // yellow
    if (score >= 70) return '#f97316' // orange
    return '#ef4444' // red
  }

  const getQualityLabel = (score: number) => {
    if (score >= 90) return 'Excellent'
    if (score >= 80) return 'Good'
    if (score >= 70) return 'Fair'
    return 'Needs Improvement'
  }

  // Show detailed report if requested
  if (showDetailedReport && analysisResult) {
    return (
      <DetailedReport 
        analysisResult={analysisResult} 
        onClose={() => setShowDetailedReport(false)} 
      />
    )
  }

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '20px'
    }}>
      <div style={{
        backgroundColor: 'rgba(15, 23, 42, 0.95)',
        borderRadius: '20px',
        padding: '30px',
        maxWidth: '800px',
        width: '100%',
        maxHeight: '90vh',
        overflow: 'auto',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(20px)',
        boxShadow: '0 25px 50px rgba(0, 0, 0, 0.5)'
      }}>
        {/* Header */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
          marginBottom: '30px'
        }}>
          <button onClick={onClose} style={{
            background: 'none',
            border: 'none',
            color: '#94a3b8',
            fontSize: '24px',
            cursor: 'pointer',
            padding: '5px',
            borderRadius: '5px',
            transition: 'all 0.3s ease'
          }} onMouseOver={(e) => { (e.target as HTMLElement).style.color = '#ef4444' }}
             onMouseOut={(e) => { (e.target as HTMLElement).style.color = '#94a3b8' }}>✕</button>
          
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '15px',
            flex: 1,
            marginLeft: '20px'
          }}>
            <div style={{
              fontSize: '32px',
              width: '50px',
              height: '50px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundColor: 'rgba(139, 92, 246, 0.2)',
              borderRadius: '12px',
              color: '#8b5cf6'
            }}>🔬</div>
            <div>
              <h2 style={{
                margin: 0,
                fontSize: '24px',
                fontWeight: '700',
                color: 'white',
                marginBottom: '5px'
              }}>Repository Analyzer</h2>
              <p style={{
                margin: 0,
                color: '#94a3b8',
                fontSize: '14px'
              }}>AI-powered comprehensive analysis with Amazon Bedrock Claude</p>
            </div>
          </div>
        </div>

        {/* Content */}
        <div style={{ marginBottom: '20px' }}>
          {!isAnalyzing && !analysisResult && (
            <form onSubmit={handleSubmit} style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '25px'
            }}>
              {/* Repository URL */}
              <div>
                <label style={{
                  display: 'block',
                  marginBottom: '8px',
                  color: 'white',
                  fontSize: '14px',
                  fontWeight: '600'
                }}>🔗 Repository URL <span style={{ color: '#ef4444' }}>*</span></label>
                <input 
                  type="url" 
                  value={repositoryUrl} 
                  onChange={(e) => setRepositoryUrl(e.target.value)}
                  placeholder="https://github.com/username/repository" 
                  style={{
                    width: '100%',
                    padding: '12px 16px',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    borderRadius: '10px',
                    color: 'white',
                    fontSize: '14px',
                    transition: 'all 0.3s ease'
                  }}
                  onFocus={(e) => { 
                    (e.target as HTMLElement).style.borderColor = '#8b5cf6'; 
                    (e.target as HTMLElement).style.boxShadow = '0 0 0 3px rgba(139, 92, 246, 0.1)' 
                  }}
                  onBlur={(e) => { 
                    (e.target as HTMLElement).style.borderColor = 'rgba(255, 255, 255, 0.2)'; 
                    (e.target as HTMLElement).style.boxShadow = 'none' 
                  }}
                />
                <p style={{
                  margin: '8px 0 0 0',
                  color: '#64748b',
                  fontSize: '12px'
                }}>Enter the URL of your Git repository (GitHub, GitLab, etc.)</p>
              </div>

              {/* GitHub Token */}
              <div>
                <label style={{
                  display: 'block',
                  marginBottom: '8px',
                  color: 'white',
                  fontSize: '14px',
                  fontWeight: '600'
                }}>🔑 GitHub Token <span style={{ 
                  color: '#64748b', 
                  fontSize: '12px', 
                  fontWeight: '400' 
                }}>Optional</span></label>
                <input 
                  type="password" 
                  value={githubToken} 
                  onChange={(e) => setGithubToken(e.target.value)}
                  placeholder="ghp_xxxxxxxxxxxxxxxxxxxx" 
                  style={{
                    width: '100%',
                    padding: '12px 16px',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    borderRadius: '10px',
                    color: 'white',
                    fontSize: '14px',
                    transition: 'all 0.3s ease'
                  }}
                  onFocus={(e) => { 
                    (e.target as HTMLElement).style.borderColor = '#8b5cf6'; 
                    (e.target as HTMLElement).style.boxShadow = '0 0 0 3px rgba(139, 92, 246, 0.1)' 
                  }}
                  onBlur={(e) => { 
                    (e.target as HTMLElement).style.borderColor = 'rgba(255, 255, 255, 0.2)'; 
                    (e.target as HTMLElement).style.boxShadow = 'none' 
                  }}
                />
                <p style={{
                  margin: '8px 0 0 0',
                  color: '#64748b',
                  fontSize: '12px'
                }}>Provide a GitHub token for private repositories and better rate limits</p>
              </div>

              {/* Analysis Info */}
              <div>
                <label style={{
                  display: 'block',
                  marginBottom: '15px',
                  color: 'white',
                  fontSize: '14px',
                  fontWeight: '600'
                }}>🎯 Analysis Overview</label>
                <div style={{
                  padding: '25px',
                  backgroundColor: 'rgba(139, 92, 246, 0.1)',
                  border: '2px solid #8b5cf6',
                  borderRadius: '15px',
                  position: 'relative'
                }}>
                  <div style={{
                    position: 'absolute',
                    top: '15px',
                    right: '15px',
                    width: '25px',
                    height: '25px',
                    backgroundColor: '#8b5cf6',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontSize: '14px',
                    fontWeight: 'bold'
                  }}>🚀</div>
                  
                  <h3 style={{
                    margin: '0 0 12px 0',
                    color: 'white',
                    fontSize: '18px',
                    fontWeight: '600'
                  }}>{analysisInfo.title}</h3>
                  <p style={{
                    margin: '0 0 15px 0',
                    color: '#94a3b8',
                    fontSize: '14px',
                    lineHeight: '1.5'
                  }}>{analysisInfo.description}</p>
                  <div style={{
                    color: '#8b5cf6',
                    fontSize: '13px',
                    fontWeight: '600',
                    marginBottom: '15px',
                    padding: '8px 12px',
                    backgroundColor: 'rgba(139, 92, 246, 0.2)',
                    borderRadius: '8px',
                    display: 'inline-block'
                  }}>⏱️ {analysisInfo.duration}</div>
                  
                  <div style={{ marginTop: '20px' }}>
                    <h4 style={{
                      margin: '0 0 12px 0',
                      color: 'white',
                      fontSize: '14px',
                      fontWeight: '600'
                    }}>What's included:</h4>
                    <div style={{
                      display: 'grid',
                      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                      gap: '8px'
                    }}>
                      {analysisInfo.features.map((feature, index) => (
                        <div key={index} style={{
                          color: '#94a3b8',
                          fontSize: '13px',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '8px'
                        }}>
                          <span style={{ 
                            color: '#8b5cf6', 
                            fontSize: '12px',
                            fontWeight: 'bold'
                          }}>✓</span>
                          {feature}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Error Display */}
              {error && (
                <div style={{
                  padding: '12px 16px',
                  backgroundColor: 'rgba(239, 68, 68, 0.1)',
                  border: '1px solid rgba(239, 68, 68, 0.3)',
                  borderRadius: '8px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px'
                }}>
                  <span style={{ fontSize: '16px' }}>⚠️</span>
                  <span style={{ color: '#fca5a5', fontSize: '14px' }}>{error}</span>
                </div>
              )}

              {/* Submit Button */}
              <button 
                type="submit" 
                disabled={!repositoryUrl.trim()}
                style={{
                  padding: '15px 30px',
                  backgroundColor: repositoryUrl.trim() ? '#8b5cf6' : 'rgba(139, 92, 246, 0.3)',
                  color: 'white',
                  border: 'none',
                  borderRadius: '12px',
                  fontSize: '16px',
                  fontWeight: '600',
                  cursor: repositoryUrl.trim() ? 'pointer' : 'not-allowed',
                  transition: 'all 0.3s ease',
                  transform: 'scale(1)',
                  boxShadow: repositoryUrl.trim() ? '0 8px 20px rgba(139, 92, 246, 0.3)' : 'none'
                }}
                onMouseOver={(e) => { 
                  if (repositoryUrl.trim()) { 
                    (e.target as HTMLElement).style.transform = 'scale(1.02)'; 
                    (e.target as HTMLElement).style.boxShadow = '0 15px 35px rgba(139, 92, 246, 0.4)' 
                  } 
                }}
                onMouseOut={(e) => { 
                  if (repositoryUrl.trim()) { 
                    (e.target as HTMLElement).style.transform = 'scale(1)'; 
                    (e.target as HTMLElement).style.boxShadow = '0 8px 20px rgba(139, 92, 246, 0.3)' 
                  } 
                }}
              >
                🚀 Start AI Analysis ✨
              </button>
            </form>
          )}

          {/* Progress Display */}
          {isAnalyzing && (
            <div style={{
              textAlign: 'center',
              padding: '40px 20px'
            }}>
              <div style={{
                fontSize: '48px',
                marginBottom: '20px',
                animation: 'spin 2s linear infinite'
              }}>🔄</div>
              <div style={{ marginBottom: '30px' }}>
                <h3 style={{
                  margin: '0 0 10px 0',
                  color: 'white',
                  fontSize: '20px',
                  fontWeight: '600'
                }}>AI Analyzing Repository</h3>
                <p style={{
                  margin: 0,
                  color: '#94a3b8',
                  fontSize: '14px'
                }}>{currentStage}</p>
              </div>
              
              {/* Progress Bar */}
              <div style={{
                width: '100%',
                height: '8px',
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
                borderRadius: '4px',
                overflow: 'hidden',
                marginBottom: '15px'
              }}>
                <div style={{
                  width: `${progress}%`,
                  height: '100%',
                  backgroundColor: '#8b5cf6',
                  borderRadius: '4px',
                  transition: 'width 0.5s ease',
                  boxShadow: '0 0 10px rgba(139, 92, 246, 0.5)'
                }}></div>
              </div>
              <p style={{
                margin: 0,
                color: '#8b5cf6',
                fontSize: '14px',
                fontWeight: '600'
              }}>{Math.round(progress)}% Complete</p>
            </div>
          )}

          {/* Results Display */}
          {analysisResult && (
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '25px'
            }}>
              {/* Header */}
              <div style={{ textAlign: 'center' }}>
                <div style={{
                  fontSize: '48px',
                  marginBottom: '15px'
                }}>🎉</div>
                <h3 style={{
                  margin: '0 0 10px 0',
                  color: 'white',
                  fontSize: '24px',
                  fontWeight: '700'
                }}>AI Analysis Complete!</h3>
                <p style={{
                  margin: 0,
                  color: '#94a3b8',
                  fontSize: '14px'
                }}>Repository: <strong style={{ color: 'white' }}>{analysisResult.repository_name}</strong></p>
              </div>

              {/* Overall Quality Score */}
              {analysisResult.overall_scores?.overall_quality_score && (
                <div style={{
                  textAlign: 'center',
                  padding: '25px',
                  backgroundColor: 'rgba(255, 255, 255, 0.05)',
                  borderRadius: '15px',
                  border: '1px solid rgba(255, 255, 255, 0.1)'
                }}>
                  <h4 style={{
                    margin: '0 0 15px 0',
                    color: 'white',
                    fontSize: '16px',
                    fontWeight: '600'
                  }}>Overall Quality Score</h4>
                  <div style={{
                    fontSize: '48px',
                    fontWeight: '700',
                    color: getQualityColor(analysisResult.overall_scores.overall_quality_score),
                    marginBottom: '10px'
                  }}>{analysisResult.overall_scores.overall_quality_score}</div>
                  <div style={{
                    color: getQualityColor(analysisResult.overall_scores.overall_quality_score),
                    fontSize: '14px',
                    fontWeight: '600'
                  }}>{getQualityLabel(analysisResult.overall_scores.overall_quality_score)}</div>
                </div>
              )}

              {/* Metrics Grid */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                gap: '15px'
              }}>
                {analysisResult.overall_scores?.architecture_score && (
                  <div style={{
                    padding: '20px',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    borderRadius: '12px',
                    textAlign: 'center',
                    border: '1px solid rgba(255, 255, 255, 0.1)'
                  }}>
                    <div style={{ fontSize: '24px', marginBottom: '8px' }}>🔧</div>
                    <h5 style={{
                      margin: '0 0 8px 0',
                      color: 'white',
                      fontSize: '14px',
                      fontWeight: '600'
                    }}>Architecture</h5>
                    <div style={{
                      color: getQualityColor(analysisResult.overall_scores.architecture_score),
                      fontSize: '18px',
                      fontWeight: '700'
                    }}>{analysisResult.overall_scores.architecture_score}%</div>
                  </div>
                )}
                
                {analysisResult.overall_scores?.security_score && (
                  <div style={{
                    padding: '20px',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    borderRadius: '12px',
                    textAlign: 'center',
                    border: '1px solid rgba(255, 255, 255, 0.1)'
                  }}>
                    <div style={{ fontSize: '24px', marginBottom: '8px' }}>🛡️</div>
                    <h5 style={{
                      margin: '0 0 8px 0',
                      color: 'white',
                      fontSize: '14px',
                      fontWeight: '600'
                    }}>Security</h5>
                    <div style={{
                      color: getQualityColor(analysisResult.overall_scores.security_score),
                      fontSize: '18px',
                      fontWeight: '700'
                    }}>{analysisResult.overall_scores.security_score}%</div>
                  </div>
                )}
                
                {analysisResult.overall_scores?.maintainability_score && (
                  <div style={{
                    padding: '20px',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    borderRadius: '12px',
                    textAlign: 'center',
                    border: '1px solid rgba(255, 255, 255, 0.1)'
                  }}>
                    <div style={{ fontSize: '24px', marginBottom: '8px' }}>📝</div>
                    <h5 style={{
                      margin: '0 0 8px 0',
                      color: 'white',
                      fontSize: '14px',
                      fontWeight: '600'
                    }}>Maintainability</h5>
                    <div style={{
                      color: getQualityColor(analysisResult.overall_scores.maintainability_score),
                      fontSize: '18px',
                      fontWeight: '700'
                    }}>{analysisResult.overall_scores.maintainability_score}%</div>
                  </div>
                )}
                
                {analysisResult.repository_overview?.lines_of_code && (
                  <div style={{
                    padding: '20px',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    borderRadius: '12px',
                    textAlign: 'center',
                    border: '1px solid rgba(255, 255, 255, 0.1)'
                  }}>
                    <div style={{ fontSize: '24px', marginBottom: '8px' }}>📊</div>
                    <h5 style={{
                      margin: '0 0 8px 0',
                      color: 'white',
                      fontSize: '14px',
                      fontWeight: '600'
                    }}>Lines of Code</h5>
                    <div style={{
                      color: '#8b5cf6',
                      fontSize: '18px',
                      fontWeight: '700'
                    }}>{analysisResult.repository_overview.lines_of_code.toLocaleString()}</div>
                  </div>
                )}
                
                {analysisResult.technical_metrics?.security_vulnerabilities !== undefined && (
                  <div style={{
                    padding: '20px',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    borderRadius: '12px',
                    textAlign: 'center',
                    border: '1px solid rgba(255, 255, 255, 0.1)'
                  }}>
                    <div style={{ fontSize: '24px', marginBottom: '8px' }}>⚠️</div>
                    <h5 style={{
                      margin: '0 0 8px 0',
                      color: 'white',
                      fontSize: '14px',
                      fontWeight: '600'
                    }}>Vulnerabilities</h5>
                    <div style={{
                      color: analysisResult.technical_metrics.security_vulnerabilities > 0 ? '#ef4444' : '#10b981',
                      fontSize: '18px',
                      fontWeight: '700'
                    }}>{analysisResult.technical_metrics.security_vulnerabilities}</div>
                  </div>
                )}
                
                {analysisResult.technical_metrics?.dependencies_outdated !== undefined && (
                  <div style={{
                    padding: '20px',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    borderRadius: '12px',
                    textAlign: 'center',
                    border: '1px solid rgba(255, 255, 255, 0.1)'
                  }}>
                    <div style={{ fontSize: '24px', marginBottom: '8px' }}>📦</div>
                    <h5 style={{
                      margin: '0 0 8px 0',
                      color: 'white',
                      fontSize: '14px',
                      fontWeight: '600'
                    }}>Outdated Deps</h5>
                    <div style={{
                      color: analysisResult.technical_metrics.dependencies_outdated > 0 ? '#f59e0b' : '#10b981',
                      fontSize: '18px',
                      fontWeight: '700'
                    }}>{analysisResult.technical_metrics.dependencies_outdated}</div>
                  </div>
                )}
              </div>

              {/* AI Insights */}
              {analysisResult.ai_insights && (
                <div style={{
                  padding: '25px',
                  backgroundColor: 'rgba(139, 92, 246, 0.1)',
                  borderRadius: '15px',
                  border: '1px solid rgba(139, 92, 246, 0.2)'
                }}>
                  <h4 style={{
                    margin: '0 0 20px 0',
                    color: 'white',
                    fontSize: '18px',
                    fontWeight: '600',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px'
                  }}>
                    🧠 AI Insights
                  </h4>
                  
                  {/* AI Error Warning */}
                  {(analysisResult as any).ai_error && (
                    <div style={{
                      padding: '15px',
                      backgroundColor: 'rgba(239, 68, 68, 0.1)',
                      border: '1px solid rgba(239, 68, 68, 0.3)',
                      borderRadius: '8px',
                      marginBottom: '20px'
                    }}>
                      <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '10px',
                        marginBottom: '10px'
                      }}>
                        <span style={{ fontSize: '16px' }}>⚠️</span>
                        <strong style={{ color: '#fca5a5', fontSize: '14px' }}>AI Analysis Error</strong>
                      </div>
                      <p style={{
                        margin: '0 0 8px 0',
                        color: '#fca5a5',
                        fontSize: '13px'
                      }}>
                        <strong>Error:</strong> {(analysisResult as any).ai_error}
                      </p>
                      {(analysisResult as any).ai_raw_response && (
                        <details style={{ marginTop: '10px' }}>
                          <summary style={{
                            color: '#fca5a5',
                            fontSize: '12px',
                            cursor: 'pointer',
                            fontWeight: '600'
                          }}>Show Raw AI Response</summary>
                          <pre style={{
                            margin: '8px 0 0 0',
                            padding: '10px',
                            backgroundColor: 'rgba(0, 0, 0, 0.3)',
                            borderRadius: '4px',
                            color: '#fca5a5',
                            fontSize: '11px',
                            overflow: 'auto',
                            maxHeight: '200px'
                          }}>{(analysisResult as any).ai_raw_response}</pre>
                        </details>
                      )}
                      <p style={{
                        margin: '8px 0 0 0',
                        color: '#94a3b8',
                        fontSize: '12px',
                        fontStyle: 'italic'
                      }}>
                        Showing fallback analysis based on repository structure and static analysis results.
                      </p>
                    </div>
                  )}
                  
                  {analysisResult.ai_insights.architecture_pattern && (
                    <div style={{ marginBottom: '15px' }}>
                      <strong style={{ color: '#8b5cf6' }}>Architecture Pattern:</strong>
                      <span style={{ color: 'white', marginLeft: '8px' }}>
                        {analysisResult.ai_insights.architecture_pattern}
                      </span>
                    </div>
                  )}
                  
                  {analysisResult.ai_insights.strengths && analysisResult.ai_insights.strengths.length > 0 && (
                    <div style={{ marginBottom: '15px' }}>
                      <strong style={{ color: '#10b981' }}>Strengths:</strong>
                      <ul style={{
                        margin: '8px 0 0 20px',
                        color: '#94a3b8',
                        fontSize: '14px'
                      }}>
                        {analysisResult.ai_insights.strengths.map((strength: string, index: number) => (
                          <li key={index}>{strength}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  
                  {analysisResult.ai_insights.recommendations && analysisResult.ai_insights.recommendations.length > 0 && (
                    <div>
                      <strong style={{ color: '#f59e0b' }}>Recommendations:</strong>
                      <ul style={{
                        margin: '8px 0 0 20px',
                        color: '#94a3b8',
                        fontSize: '14px'
                      }}>
                        {analysisResult.ai_insights.recommendations.map((rec: string, index: number) => (
                          <li key={index}>{rec}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {/* Executive Summary */}
              {analysisResult.executive_summary && (
                <div style={{
                  padding: '25px',
                  backgroundColor: 'rgba(255, 255, 255, 0.05)',
                  borderRadius: '15px',
                  border: '1px solid rgba(255, 255, 255, 0.1)'
                }}>
                  <h4 style={{
                    margin: '0 0 15px 0',
                    color: 'white',
                    fontSize: '18px',
                    fontWeight: '600',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px'
                  }}>
                    📋 Executive Summary
                  </h4>
                  <p style={{
                    margin: 0,
                    color: '#94a3b8',
                    fontSize: '14px',
                    lineHeight: '1.6'
                  }}>{analysisResult.executive_summary}</p>
                </div>
              )}

              {/* Action Buttons */}
              <div style={{
                display: 'flex',
                gap: '15px',
                justifyContent: 'center',
                flexWrap: 'wrap'
              }}>
                <button 
                  onClick={() => { 
                    setAnalysisResult(null); 
                    setRepositoryUrl(''); 
                    setGithubToken(''); 
                    setError(''); 
                  }}
                  style={{
                    padding: '12px 24px',
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    color: 'white',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    borderRadius: '8px',
                    fontSize: '14px',
                    fontWeight: '600',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease'
                  }}
                  onMouseOver={(e) => { (e.target as HTMLElement).style.background = 'rgba(255, 255, 255, 0.2)' }}
                  onMouseOut={(e) => { (e.target as HTMLElement).style.background = 'rgba(255, 255, 255, 0.1)' }}
                >
                  🔄 Analyze Another
                </button>
                <button 
                  onClick={() => setShowDetailedReport(true)}
                  style={{
                    padding: '12px 24px',
                    backgroundColor: '#8b5cf6',
                    color: 'white',
                    border: 'none',
                    borderRadius: '8px',
                    fontSize: '14px',
                    fontWeight: '600',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    transform: 'scale(1)',
                    boxShadow: '0 8px 20px rgba(139, 92, 246, 0.3)'
                  }}
                  onMouseOver={(e) => { 
                    (e.target as HTMLElement).style.transform = 'scale(1.05)'; 
                    (e.target as HTMLElement).style.boxShadow = '0 12px 30px rgba(139, 92, 246, 0.4)' 
                  }}
                  onMouseOut={(e) => { 
                    (e.target as HTMLElement).style.transform = 'scale(1)'; 
                    (e.target as HTMLElement).style.boxShadow = '0 8px 20px rgba(139, 92, 246, 0.3)' 
                  }}
                >
                  📊 View Full Report
                </button>
                <button 
                  onClick={async () => {
                    try {
                      const response = await fetch(`http://localhost:8000/api/analysis/${analysisResult.id}/report`)
                      if (response.ok) {
                        const blob = await response.blob()
                        const url = window.URL.createObjectURL(blob)
                        const a = document.createElement('a')
                        a.href = url
                        a.download = `mVISE_analysis_${analysisResult.repository_name}_${new Date().toISOString().split('T')[0]}.pdf`
                        document.body.appendChild(a)
                        a.click()
                        window.URL.revokeObjectURL(url)
                        document.body.removeChild(a)
                      } else {
                        alert('Failed to generate report')
                      }
                    } catch (error) {
                      console.error('Report download error:', error)
                      alert('Failed to download report')
                    }
                  }}
                  style={{
                    padding: '12px 24px',
                    backgroundColor: '#10b981',
                    color: 'white',
                    border: 'none',
                    borderRadius: '8px',
                    fontSize: '14px',
                    fontWeight: '600',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    transform: 'scale(1)',
                    boxShadow: '0 8px 20px rgba(16, 185, 129, 0.3)'
                  }}
                  onMouseOver={(e) => { 
                    (e.target as HTMLElement).style.transform = 'scale(1.05)'; 
                    (e.target as HTMLElement).style.boxShadow = '0 12px 30px rgba(16, 185, 129, 0.4)' 
                  }}
                  onMouseOut={(e) => { 
                    (e.target as HTMLElement).style.transform = 'scale(1)'; 
                    (e.target as HTMLElement).style.boxShadow = '0 8px 20px rgba(16, 185, 129, 0.3)' 
                  }}
                >
                  📄 Download PDF Report
                </button>
              </div>
            </div>
          )}
        </div>
        
        <style jsx>{`
          @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
          
          ::-webkit-scrollbar {
            width: 8px;
          }
          
          ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
          }
          
          ::-webkit-scrollbar-thumb {
            background: rgba(139, 92, 246, 0.5);
            border-radius: 4px;
          }
          
          ::-webkit-scrollbar-thumb:hover {
            background: rgba(139, 92, 246, 0.7);
          }
        `}</style>
      </div>
    </div>
  )
} 