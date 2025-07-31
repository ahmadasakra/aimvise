'use client'

import React, { useState } from 'react'

interface DetailedReportProps {
  analysisResult: any
  onClose: () => void
}

export default function DetailedReport({ analysisResult, onClose }: DetailedReportProps) {
  const [activeTab, setActiveTab] = useState('overview')

  const tabs = [
    { id: 'overview', label: '📊 Executive Summary', icon: '📊' },
    { id: 'architecture', label: '🏗️ Architecture', icon: '🏗️' },
    { id: 'technology', label: '⚙️ Technology Stack', icon: '⚙️' },
    { id: 'quality', label: '🔍 Code Quality', icon: '🔍' },
    { id: 'security', label: '🛡️ Security', icon: '🛡️' },
    { id: 'business', label: '💼 Business Impact', icon: '💼' },
    { id: 'recommendations', label: '🎯 Recommendations', icon: '🎯' }
  ]

  const getQualityColor = (score: number) => {
    if (score >= 90) return '#10b981'
    if (score >= 80) return '#f59e0b'
    if (score >= 70) return '#f97316'
    return '#ef4444'
  }

  const getQualityLabel = (score: number) => {
    if (score >= 90) return 'Excellent'
    if (score >= 80) return 'Good'
    if (score >= 70) return 'Fair'
    return 'Needs Improvement'
  }

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.9)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 2000,
      padding: '20px'
    }}>
      <div style={{
        backgroundColor: 'rgba(15, 23, 42, 0.98)',
        borderRadius: '20px',
        maxWidth: '1200px',
        width: '100%',
        maxHeight: '95vh',
        overflow: 'hidden',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(20px)',
        boxShadow: '0 25px 50px rgba(0, 0, 0, 0.5)',
        display: 'flex',
        flexDirection: 'column'
      }}>
        {/* Header */}
        <div style={{
          padding: '25px 30px',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
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
            }}>📋</div>
            <div>
              <h2 style={{
                margin: 0,
                fontSize: '24px',
                fontWeight: '700',
                color: 'white'
              }}>Detailed Analysis Report</h2>
              <p style={{
                margin: '5px 0 0 0',
                color: '#94a3b8',
                fontSize: '14px'
              }}>Repository: {analysisResult.repository_name}</p>
            </div>
          </div>
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
        </div>

        {/* Tabs */}
        <div style={{
          padding: '0 30px',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
          overflowX: 'auto'
        }}>
          <div style={{
            display: 'flex',
            gap: '5px',
            padding: '15px 0'
          }}>
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  padding: '10px 20px',
                  backgroundColor: activeTab === tab.id ? 'rgba(139, 92, 246, 0.2)' : 'rgba(255, 255, 255, 0.05)',
                  border: activeTab === tab.id ? '1px solid #8b5cf6' : '1px solid rgba(255, 255, 255, 0.1)',
                  borderRadius: '8px',
                  color: activeTab === tab.id ? 'white' : '#94a3b8',
                  fontSize: '14px',
                  fontWeight: activeTab === tab.id ? '600' : '400',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  whiteSpace: 'nowrap'
                }}
                onMouseOver={(e) => {
                  if (activeTab !== tab.id) {
                    (e.target as HTMLElement).style.background = 'rgba(255, 255, 255, 0.1)'
                  }
                }}
                onMouseOut={(e) => {
                  if (activeTab !== tab.id) {
                    (e.target as HTMLElement).style.background = 'rgba(255, 255, 255, 0.05)'
                  }
                }}
              >
                {tab.icon} {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        <div style={{
          flex: 1,
          overflow: 'auto',
          padding: '30px'
        }}>
          {activeTab === 'overview' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
              {/* Executive Summary */}
              <div style={{
                padding: '25px',
                backgroundColor: 'rgba(139, 92, 246, 0.1)',
                borderRadius: '15px',
                border: '1px solid rgba(139, 92, 246, 0.2)'
              }}>
                <h3 style={{
                  margin: '0 0 15px 0',
                  color: 'white',
                  fontSize: '20px',
                  fontWeight: '600',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px'
                }}>
                  🎯 Executive Summary
                </h3>
                <p style={{
                  margin: 0,
                  color: '#94a3b8',
                  fontSize: '16px',
                  lineHeight: '1.6'
                }}>
                  {analysisResult.executive_summary || 
                    `This repository analysis provides a comprehensive assessment of the codebase quality, 
                    architecture patterns, and technical debt. The analysis covers ${analysisResult.repository_overview?.lines_of_code?.toLocaleString() || 'unknown'} 
                    lines of code across ${analysisResult.repository_overview?.total_files || 'unknown'} files.`}
                </p>
              </div>

              {/* Overall Scores */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '20px'
              }}>
                {analysisResult.overall_scores?.overall_quality_score && (
                  <div style={{
                    padding: '25px',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    borderRadius: '15px',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    textAlign: 'center'
                  }}>
                    <h4 style={{
                      margin: '0 0 15px 0',
                      color: 'white',
                      fontSize: '16px',
                      fontWeight: '600'
                    }}>Overall Quality</h4>
                    <div style={{
                      fontSize: '36px',
                      fontWeight: '700',
                      color: getQualityColor(analysisResult.overall_scores.overall_quality_score),
                      marginBottom: '8px'
                    }}>{analysisResult.overall_scores.overall_quality_score}</div>
                    <div style={{
                      color: getQualityColor(analysisResult.overall_scores.overall_quality_score),
                      fontSize: '14px',
                      fontWeight: '600'
                    }}>{getQualityLabel(analysisResult.overall_scores.overall_quality_score)}</div>
                  </div>
                )}

                {analysisResult.overall_scores?.architecture_score && (
                  <div style={{
                    padding: '25px',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    borderRadius: '15px',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    textAlign: 'center'
                  }}>
                    <h4 style={{
                      margin: '0 0 15px 0',
                      color: 'white',
                      fontSize: '16px',
                      fontWeight: '600'
                    }}>Architecture</h4>
                    <div style={{
                      fontSize: '36px',
                      fontWeight: '700',
                      color: getQualityColor(analysisResult.overall_scores.architecture_score),
                      marginBottom: '8px'
                    }}>{analysisResult.overall_scores.architecture_score}%</div>
                    <div style={{
                      color: getQualityColor(analysisResult.overall_scores.architecture_score),
                      fontSize: '14px',
                      fontWeight: '600'
                    }}>{getQualityLabel(analysisResult.overall_scores.architecture_score)}</div>
                  </div>
                )}

                {analysisResult.overall_scores?.security_score && (
                  <div style={{
                    padding: '25px',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    borderRadius: '15px',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    textAlign: 'center'
                  }}>
                    <h4 style={{
                      margin: '0 0 15px 0',
                      color: 'white',
                      fontSize: '16px',
                      fontWeight: '600'
                    }}>Security</h4>
                    <div style={{
                      fontSize: '36px',
                      fontWeight: '700',
                      color: getQualityColor(analysisResult.overall_scores.security_score),
                      marginBottom: '8px'
                    }}>{analysisResult.overall_scores.security_score}%</div>
                    <div style={{
                      color: getQualityColor(analysisResult.overall_scores.security_score),
                      fontSize: '14px',
                      fontWeight: '600'
                    }}>{getQualityLabel(analysisResult.overall_scores.security_score)}</div>
                  </div>
                )}

                {analysisResult.overall_scores?.maintainability_score && (
                  <div style={{
                    padding: '25px',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    borderRadius: '15px',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    textAlign: 'center'
                  }}>
                    <h4 style={{
                      margin: '0 0 15px 0',
                      color: 'white',
                      fontSize: '16px',
                      fontWeight: '600'
                    }}>Maintainability</h4>
                    <div style={{
                      fontSize: '36px',
                      fontWeight: '700',
                      color: getQualityColor(analysisResult.overall_scores.maintainability_score),
                      marginBottom: '8px'
                    }}>{analysisResult.overall_scores.maintainability_score}%</div>
                    <div style={{
                      color: getQualityColor(analysisResult.overall_scores.maintainability_score),
                      fontSize: '14px',
                      fontWeight: '600'
                    }}>{getQualityLabel(analysisResult.overall_scores.maintainability_score)}</div>
                  </div>
                )}
              </div>

              {/* Key Metrics */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                gap: '15px'
              }}>
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
                  }}>{analysisResult.repository_overview?.lines_of_code?.toLocaleString() || 'N/A'}</div>
                </div>

                <div style={{
                  padding: '20px',
                  backgroundColor: 'rgba(255, 255, 255, 0.05)',
                  borderRadius: '12px',
                  textAlign: 'center',
                  border: '1px solid rgba(255, 255, 255, 0.1)'
                }}>
                  <div style={{ fontSize: '24px', marginBottom: '8px' }}>📁</div>
                  <h5 style={{
                    margin: '0 0 8px 0',
                    color: 'white',
                    fontSize: '14px',
                    fontWeight: '600'
                  }}>Total Files</h5>
                  <div style={{
                    color: '#8b5cf6',
                    fontSize: '18px',
                    fontWeight: '700'
                  }}>{analysisResult.repository_overview?.total_files || 'N/A'}</div>
                </div>

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
                    color: analysisResult.technical_metrics?.security_vulnerabilities > 0 ? '#ef4444' : '#10b981',
                    fontSize: '18px',
                    fontWeight: '700'
                  }}>{analysisResult.technical_metrics?.security_vulnerabilities || 0}</div>
                </div>

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
                    color: analysisResult.technical_metrics?.dependencies_outdated > 0 ? '#f59e0b' : '#10b981',
                    fontSize: '18px',
                    fontWeight: '700'
                  }}>{analysisResult.technical_metrics?.dependencies_outdated || 0}</div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'architecture' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
              <div style={{
                padding: '25px',
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                borderRadius: '15px',
                border: '1px solid rgba(255, 255, 255, 0.1)'
              }}>
                <h3 style={{
                  margin: '0 0 20px 0',
                  color: 'white',
                  fontSize: '20px',
                  fontWeight: '600'
                }}>🏗️ Architecture Analysis</h3>
                
                {analysisResult.ai_insights?.architecture_pattern && (
                  <div style={{ marginBottom: '20px' }}>
                    <h4 style={{
                      margin: '0 0 10px 0',
                      color: '#8b5cf6',
                      fontSize: '16px',
                      fontWeight: '600'
                    }}>Architecture Pattern</h4>
                    <p style={{
                      margin: 0,
                      color: 'white',
                      fontSize: '16px'
                    }}>{analysisResult.ai_insights.architecture_pattern}</p>
                  </div>
                )}

                {analysisResult.ai_insights?.strengths && analysisResult.ai_insights.strengths.length > 0 && (
                  <div style={{ marginBottom: '20px' }}>
                    <h4 style={{
                      margin: '0 0 10px 0',
                      color: '#10b981',
                      fontSize: '16px',
                      fontWeight: '600'
                    }}>Architecture Strengths</h4>
                    <ul style={{
                      margin: 0,
                      padding: '0 0 0 20px',
                      color: '#94a3b8'
                    }}>
                      {analysisResult.ai_insights.strengths.map((strength: string, index: number) => (
                        <li key={index} style={{ marginBottom: '5px' }}>{strength}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {analysisResult.ai_insights?.weaknesses && analysisResult.ai_insights.weaknesses.length > 0 && (
                  <div>
                    <h4 style={{
                      margin: '0 0 10px 0',
                      color: '#ef4444',
                      fontSize: '16px',
                      fontWeight: '600'
                    }}>Architecture Concerns</h4>
                    <ul style={{
                      margin: 0,
                      padding: '0 0 0 20px',
                      color: '#94a3b8'
                    }}>
                      {analysisResult.ai_insights.weaknesses.map((weakness: string, index: number) => (
                        <li key={index} style={{ marginBottom: '5px' }}>{weakness}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'technology' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
              <div style={{
                padding: '25px',
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                borderRadius: '15px',
                border: '1px solid rgba(255, 255, 255, 0.1)'
              }}>
                <h3 style={{
                  margin: '0 0 20px 0',
                  color: 'white',
                  fontSize: '20px',
                  fontWeight: '600'
                }}>⚙️ Technology Stack Analysis</h3>

                {analysisResult.repository_overview?.languages && (
                  <div style={{ marginBottom: '20px' }}>
                    <h4 style={{
                      margin: '0 0 10px 0',
                      color: '#8b5cf6',
                      fontSize: '16px',
                      fontWeight: '600'
                    }}>Programming Languages</h4>
                    <div style={{
                      display: 'flex',
                      flexWrap: 'wrap',
                      gap: '10px'
                    }}>
                      {analysisResult.repository_overview.languages.map((lang: string, index: number) => (
                        <span key={index} style={{
                          padding: '6px 12px',
                          backgroundColor: 'rgba(139, 92, 246, 0.2)',
                          color: '#8b5cf6',
                          borderRadius: '6px',
                          fontSize: '14px',
                          fontWeight: '500'
                        }}>{lang}</span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Detailed Technology Analysis */}
                <div style={{ marginBottom: '20px' }}>
                  <h4 style={{
                    margin: '0 0 10px 0',
                    color: '#8b5cf6',
                    fontSize: '16px',
                    fontWeight: '600'
                  }}>Technology Stack Breakdown</h4>
                  
                  <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                    gap: '15px'
                  }}>
                    <div style={{
                      padding: '15px',
                      backgroundColor: 'rgba(255, 255, 255, 0.05)',
                      borderRadius: '10px',
                      border: '1px solid rgba(255, 255, 255, 0.1)'
                    }}>
                      <h5 style={{
                        margin: '0 0 8px 0',
                        color: 'white',
                        fontSize: '14px',
                        fontWeight: '600'
                      }}>Frontend Technologies</h5>
                      <div style={{
                        color: '#94a3b8',
                        fontSize: '12px'
                      }}>
                        {analysisResult.ai_insights?.technology_stack?.frontend?.join(', ') || 'Not detected'}
                      </div>
                    </div>
                    
                    <div style={{
                      padding: '15px',
                      backgroundColor: 'rgba(255, 255, 255, 0.05)',
                      borderRadius: '10px',
                      border: '1px solid rgba(255, 255, 255, 0.1)'
                    }}>
                      <h5 style={{
                        margin: '0 0 8px 0',
                        color: 'white',
                        fontSize: '14px',
                        fontWeight: '600'
                      }}>Backend Technologies</h5>
                      <div style={{
                        color: '#94a3b8',
                        fontSize: '12px'
                      }}>
                        {analysisResult.ai_insights?.technology_stack?.backend?.join(', ') || 'Not detected'}
                      </div>
                    </div>
                    
                    <div style={{
                      padding: '15px',
                      backgroundColor: 'rgba(255, 255, 255, 0.05)',
                      borderRadius: '10px',
                      border: '1px solid rgba(255, 255, 255, 0.1)'
                    }}>
                      <h5 style={{
                        margin: '0 0 8px 0',
                        color: 'white',
                        fontSize: '14px',
                        fontWeight: '600'
                      }}>Database Technologies</h5>
                      <div style={{
                        color: '#94a3b8',
                        fontSize: '12px'
                      }}>
                        {analysisResult.ai_insights?.technology_stack?.database?.join(', ') || 'Not detected'}
                      </div>
                    </div>
                    
                    <div style={{
                      padding: '15px',
                      backgroundColor: 'rgba(255, 255, 255, 0.05)',
                      borderRadius: '10px',
                      border: '1px solid rgba(255, 255, 255, 0.1)'
                    }}>
                      <h5 style={{
                        margin: '0 0 8px 0',
                        color: 'white',
                        fontSize: '14px',
                        fontWeight: '600'
                      }}>Build Tools</h5>
                      <div style={{
                        color: '#94a3b8',
                        fontSize: '12px'
                      }}>
                        {analysisResult.ai_insights?.technology_stack?.build_tools?.join(', ') || 'Not detected'}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Version Analysis */}
                {analysisResult.ai_insights?.technology_stack?.outdated_components && (
                  <div style={{ marginBottom: '20px' }}>
                    <h4 style={{
                      margin: '0 0 10px 0',
                      color: '#f59e0b',
                      fontSize: '16px',
                      fontWeight: '600'
                    }}>⚠️ Outdated Components</h4>
                    <div style={{
                      padding: '15px',
                      backgroundColor: 'rgba(245, 158, 11, 0.1)',
                      borderRadius: '10px',
                      border: '1px solid rgba(245, 158, 11, 0.2)',
                      color: '#fbbf24',
                      fontSize: '14px'
                    }}>
                      {analysisResult.ai_insights.technology_stack.outdated_components.join(', ')}
                    </div>
                  </div>
                )}

                {/* Environment Strategy */}
                {analysisResult.ai_insights?.environment_strategy && (
                  <div>
                    <h4 style={{
                      margin: '0 0 10px 0',
                      color: '#8b5cf6',
                      fontSize: '16px',
                      fontWeight: '600'
                    }}>Environment Strategy</h4>
                    <div style={{
                      display: 'grid',
                      gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                      gap: '10px'
                    }}>
                      <div style={{
                        padding: '10px',
                        backgroundColor: 'rgba(255, 255, 255, 0.05)',
                        borderRadius: '8px',
                        textAlign: 'center'
                      }}>
                        <div style={{ color: '#10b981', fontSize: '12px', fontWeight: '600' }}>Development</div>
                        <div style={{ color: '#94a3b8', fontSize: '11px' }}>
                          {analysisResult.ai_insights.environment_strategy.development || 'Not specified'}
                        </div>
                      </div>
                      <div style={{
                        padding: '10px',
                        backgroundColor: 'rgba(255, 255, 255, 0.05)',
                        borderRadius: '8px',
                        textAlign: 'center'
                      }}>
                        <div style={{ color: '#f59e0b', fontSize: '12px', fontWeight: '600' }}>Staging</div>
                        <div style={{ color: '#94a3b8', fontSize: '11px' }}>
                          {analysisResult.ai_insights.environment_strategy.staging || 'Not specified'}
                        </div>
                      </div>
                      <div style={{
                        padding: '10px',
                        backgroundColor: 'rgba(255, 255, 255, 0.05)',
                        borderRadius: '8px',
                        textAlign: 'center'
                      }}>
                        <div style={{ color: '#ef4444', fontSize: '12px', fontWeight: '600' }}>Production</div>
                        <div style={{ color: '#94a3b8', fontSize: '11px' }}>
                          {analysisResult.ai_insights.environment_strategy.production || 'Not specified'}
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'quality' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
              <div style={{
                padding: '25px',
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                borderRadius: '15px',
                border: '1px solid rgba(255, 255, 255, 0.1)'
              }}>
                <h3 style={{
                  margin: '0 0 20px 0',
                  color: 'white',
                  fontSize: '20px',
                  fontWeight: '600'
                }}>🔍 Code Quality Analysis</h3>

                {analysisResult.technical_metrics?.complexity_metrics && (
                  <div style={{ marginBottom: '20px' }}>
                    <h4 style={{
                      margin: '0 0 10px 0',
                      color: '#8b5cf6',
                      fontSize: '16px',
                      fontWeight: '600'
                    }}>Complexity Metrics</h4>
                    <div style={{
                      display: 'grid',
                      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                      gap: '15px'
                    }}>
                      {analysisResult.technical_metrics.complexity_metrics.average_complexity && (
                        <div style={{
                          padding: '15px',
                          backgroundColor: 'rgba(255, 255, 255, 0.05)',
                          borderRadius: '10px',
                          textAlign: 'center'
                        }}>
                          <div style={{
                            color: 'white',
                            fontSize: '24px',
                            fontWeight: '700',
                            marginBottom: '5px'
                          }}>{analysisResult.technical_metrics.complexity_metrics.average_complexity}</div>
                          <div style={{
                            color: '#94a3b8',
                            fontSize: '12px'
                          }}>Avg Complexity</div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {analysisResult.technical_metrics?.code_smells && (
                  <div>
                    <h4 style={{
                      margin: '0 0 10px 0',
                      color: '#f59e0b',
                      fontSize: '16px',
                      fontWeight: '600'
                    }}>Code Quality Issues</h4>
                    <div style={{
                      color: '#94a3b8',
                      fontSize: '14px'
                    }}>
                      {analysisResult.technical_metrics.code_smells} code smells detected
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'security' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
              <div style={{
                padding: '25px',
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                borderRadius: '15px',
                border: '1px solid rgba(255, 255, 255, 0.1)'
              }}>
                <h3 style={{
                  margin: '0 0 20px 0',
                  color: 'white',
                  fontSize: '20px',
                  fontWeight: '600'
                }}>🛡️ Security Analysis</h3>

                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                  gap: '15px',
                  marginBottom: '20px'
                }}>
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
                      color: analysisResult.technical_metrics?.security_vulnerabilities > 0 ? '#ef4444' : '#10b981',
                      fontSize: '24px',
                      fontWeight: '700'
                    }}>{analysisResult.technical_metrics?.security_vulnerabilities || 0}</div>
                  </div>

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
                    }}>Outdated Dependencies</h5>
                    <div style={{
                      color: analysisResult.technical_metrics?.dependencies_outdated > 0 ? '#f59e0b' : '#10b981',
                      fontSize: '24px',
                      fontWeight: '700'
                    }}>{analysisResult.technical_metrics?.dependencies_outdated || 0}</div>
                  </div>
                </div>

                {analysisResult.overall_scores?.security_score && (
                  <div style={{
                    padding: '20px',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    borderRadius: '12px',
                    border: '1px solid rgba(255, 255, 255, 0.1)'
                  }}>
                    <h4 style={{
                      margin: '0 0 10px 0',
                      color: getQualityColor(analysisResult.overall_scores.security_score),
                      fontSize: '16px',
                      fontWeight: '600'
                    }}>Security Score: {analysisResult.overall_scores.security_score}%</h4>
                    <p style={{
                      margin: 0,
                      color: '#94a3b8',
                      fontSize: '14px'
                    }}>
                      {getQualityLabel(analysisResult.overall_scores.security_score)} security posture
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'business' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
              <div style={{
                padding: '25px',
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                borderRadius: '15px',
                border: '1px solid rgba(255, 255, 255, 0.1)'
              }}>
                <h3 style={{
                  margin: '0 0 20px 0',
                  color: 'white',
                  fontSize: '20px',
                  fontWeight: '600'
                }}>💼 Business Impact Analysis</h3>

                {analysisResult.business_impact && (
                  <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                    gap: '20px'
                  }}>
                    {analysisResult.business_impact.technical_debt_hours && (
                      <div style={{
                        padding: '20px',
                        backgroundColor: 'rgba(255, 255, 255, 0.05)',
                        borderRadius: '12px',
                        textAlign: 'center',
                        border: '1px solid rgba(255, 255, 255, 0.1)'
                      }}>
                        <div style={{ fontSize: '24px', marginBottom: '8px' }}>⏰</div>
                        <h5 style={{
                          margin: '0 0 8px 0',
                          color: 'white',
                          fontSize: '14px',
                          fontWeight: '600'
                        }}>Technical Debt</h5>
                        <div style={{
                          color: '#f59e0b',
                          fontSize: '20px',
                          fontWeight: '700'
                        }}>{analysisResult.business_impact.technical_debt_hours}h</div>
                      </div>
                    )}

                    {analysisResult.business_impact.development_velocity && (
                      <div style={{
                        padding: '20px',
                        backgroundColor: 'rgba(255, 255, 255, 0.05)',
                        borderRadius: '12px',
                        textAlign: 'center',
                        border: '1px solid rgba(255, 255, 255, 0.1)'
                      }}>
                        <div style={{ fontSize: '24px', marginBottom: '8px' }}>🚀</div>
                        <h5 style={{
                          margin: '0 0 8px 0',
                          color: 'white',
                          fontSize: '14px',
                          fontWeight: '600'
                        }}>Development Velocity</h5>
                        <div style={{
                          color: '#8b5cf6',
                          fontSize: '20px',
                          fontWeight: '700',
                          textTransform: 'capitalize'
                        }}>{analysisResult.business_impact.development_velocity}</div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'recommendations' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
              <div style={{
                padding: '25px',
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                borderRadius: '15px',
                border: '1px solid rgba(255, 255, 255, 0.1)'
              }}>
                <h3 style={{
                  margin: '0 0 20px 0',
                  color: 'white',
                  fontSize: '20px',
                  fontWeight: '600'
                }}>🎯 Recommendations & Next Steps</h3>

                {analysisResult.ai_insights?.recommendations && analysisResult.ai_insights.recommendations.length > 0 && (
                  <div style={{ marginBottom: '20px' }}>
                    <h4 style={{
                      margin: '0 0 15px 0',
                      color: '#8b5cf6',
                      fontSize: '16px',
                      fontWeight: '600'
                    }}>Priority Recommendations</h4>
                    <div style={{
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '10px'
                    }}>
                      {analysisResult.ai_insights.recommendations.map((rec: string, index: number) => (
                        <div key={index} style={{
                          padding: '15px',
                          backgroundColor: 'rgba(139, 92, 246, 0.1)',
                          borderRadius: '10px',
                          border: '1px solid rgba(139, 92, 246, 0.2)',
                          display: 'flex',
                          alignItems: 'flex-start',
                          gap: '10px'
                        }}>
                          <div style={{
                            color: '#8b5cf6',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            minWidth: '20px'
                          }}>{index + 1}.</div>
                          <div style={{
                            color: '#94a3b8',
                            fontSize: '14px',
                            lineHeight: '1.5'
                          }}>{rec}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {analysisResult.investment_recommendations && analysisResult.investment_recommendations.length > 0 && (
                  <div>
                    <h4 style={{
                      margin: '0 0 15px 0',
                      color: '#10b981',
                      fontSize: '16px',
                      fontWeight: '600'
                    }}>Investment Recommendations</h4>
                    <div style={{
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '10px'
                    }}>
                      {analysisResult.investment_recommendations.map((rec: any, index: number) => (
                        <div key={index} style={{
                          padding: '15px',
                          backgroundColor: 'rgba(16, 185, 129, 0.1)',
                          borderRadius: '10px',
                          border: '1px solid rgba(16, 185, 129, 0.2)'
                        }}>
                          <div style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            marginBottom: '8px'
                          }}>
                            <h5 style={{
                              margin: 0,
                              color: 'white',
                              fontSize: '14px',
                              fontWeight: '600'
                            }}>{rec.task}</h5>
                            <span style={{
                              padding: '4px 8px',
                              backgroundColor: 'rgba(16, 185, 129, 0.2)',
                              color: '#10b981',
                              borderRadius: '4px',
                              fontSize: '12px',
                              fontWeight: '600'
                            }}>Priority {rec.priority}</span>
                          </div>
                          <div style={{
                            display: 'flex',
                            gap: '15px',
                            fontSize: '12px',
                            color: '#94a3b8'
                          }}>
                            <span>Effort: {rec.effort_hours}h</span>
                            <span>Value: {rec.business_value}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        <style jsx>{`
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