#!/usr/bin/env python3
"""Test PDF service fix for vulnerable_deps error"""

from app.services.pdf_service import PDFService

def test_pdf_fix():
    print("🔧 Testing PDF Service Fix...")
    
    # Create minimal test data that would cause the vulnerable_deps error
    analysis_result = {
        'id': 'test_fix',
        'repository_url': 'https://github.com/test/repo',
        'status': 'completed',
        'repository_overview': {
            'name': 'Test Repository',
            'description': 'Test fix for vulnerable_deps',
            'languages': [{'name': 'Python', 'percentage': 100}],
            'total_files': 10,
            'total_lines': 1000,
            'lines_of_code': 1000
        },
        'technical_metrics': {
            'code_quality_score': 7.5,
            'security_score': 8.0,
            'maintainability_score': 6.5,
            'security_vulnerabilities': 2,
            'dependencies_outdated': 3,
            'dependencies_total': 15,
            'vulnerable_dependencies': 1,  # This was missing before
            'complexity_metrics': {
                'average_complexity': 3.2,
                'high_complexity_count': 2
            }
        },
        'architecture': {
            'architecture_maturity': {
                'overall_score': 6.5,
                'level': '🥈 INTERMEDIATE (Good)',
                'breakdown': {
                    'design_patterns': 4.0,
                    'solid_principles': 6.5,
                    'clean_architecture': 7.0,
                    'coupling_quality': 5.5,
                    'api_design': 6.0,
                    'ddd_implementation': 7.5
                }
            },
            'design_patterns_analysis': {
                'score': 4.0,
                'detected_patterns': {
                    'creational': {
                        'factory_method': {
                            'confidence': 0.8,
                            'matches': [
                                {'file': 'factory.py', 'line': 10, 'match': 'def create_instance'}
                            ]
                        }
                    }
                }
            },
            'solid_principles_analysis': {
                'score': 6.5,
                'total_violations': 5,
                'total_good_practices': 8,
                'principles': {
                    'single_responsibility': {
                        'score': 7.0,
                        'violations': [
                            {'file': 'manager.py', 'line': 25, 'pattern': 'class UserManager'}
                        ],
                        'good_practices': [
                            {'file': 'user.py', 'line': 15, 'pattern': 'class User'}
                        ]
                    }
                }
            },
            'coupling_cohesion_metrics': {
                'score': 5.5,
                'average_instability': 0.65,
                'high_coupling_classes': ['UserManager', 'DataProcessor'],
                'coupling_details': {
                    'UserManager': {
                        'afferent_coupling': 5,
                        'efferent_coupling': 8,
                        'instability': 0.85,
                        'total_dependencies': 13
                    }
                }
            },
            'technical_debt': {
                'total_debt_hours': 45,
                'critical_issues': 2,
                'debt_ratio': 0.08
            },
            'refactoring_priorities': [
                {'class': 'UserManager', 'priority': 'High', 'reason': 'High coupling'}
            ]
        },
        'ai_insights': {
            'summary': 'Test repository with moderate architecture quality',
            'key_strengths': ['Good structure', 'Clean code'],
            'areas_for_improvement': ['Reduce coupling', 'Add patterns']
        }
    }
    
    try:
        # Test PDF generation
        pdf_service = PDFService()
        output_path = 'test_fix_report.pdf'
        
        print("📄 Generating test PDF...")
        result_path = pdf_service.generate_report(analysis_result, output_path)
        
        print(f"✅ PDF generated successfully: {result_path}")
        
        # Check file exists and has reasonable size
        import os
        if os.path.exists(result_path):
            file_size = os.path.getsize(result_path) / 1024
            print(f"📊 File size: {file_size:.1f} KB")
            print("🎉 Fix successful - vulnerable_deps error resolved!")
            return True
        else:
            print("❌ PDF file not created")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_pdf_fix()
    exit(0 if success else 1) 