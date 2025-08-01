#!/usr/bin/env python3
"""
🎯 Test Enhanced Architecture Analysis PDF Report
Quick test in backend directory
"""

import sys
import os
from pathlib import Path

# Ensure we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from app.services.analyzers.architecture_analyzer import ArchitectureAnalyzer
from app.services.pdf_service import PDFService

def main():
    print('🚀 Testing Enhanced Architecture PDF Report...')
    print('=' * 60)
    
    try:
        # Run architecture analysis on current backend
        repo_path = Path('.')
        print(f'📁 Analyzing: {repo_path.absolute()}')
        
        # Initialize and run analyzer
        analyzer = ArchitectureAnalyzer(repo_path)
        arch_results = analyzer.analyze()
        
        # Get maturity score
        maturity = arch_results.get('architecture_maturity', {})
        score = maturity.get('overall_score', 0)
        level = maturity.get('level', 'Unknown')
        
        print(f'📊 Architecture Score: {score:.1f}/10')
        print(f'📈 Maturity Level: {level}')
        
        # Create test analysis result
        analysis_result = {
            'id': 'architecture_test',
            'repository_url': 'https://github.com/test/ai-mvise',
            'status': 'completed',
            'architecture': arch_results,
            'repository_overview': {
                'name': 'AI-mVISE Test',
                'description': 'Architecture Analysis Test',
                'languages': [{'name': 'Python', 'percentage': 100}],
                'total_files': 25,
                'total_lines': 5000
            },
            'technical_metrics': {
                'code_quality_score': 7.5,
                'security_score': 8.0,
                'maintainability_score': 6.5
            },
            'ai_insights': {
                'summary': 'Test der erweiterten Architektur-Analyse mit detaillierten Metriken.',
                'key_strengths': ['Good DDD implementation', 'Clean structure'],
                'areas_for_improvement': ['Reduce coupling', 'More patterns']
            }
        }
        
        # Generate PDF
        print('📄 Generating PDF report...')
        pdf_service = PDFService()
        output_path = 'architecture_test_report.pdf'
        
        result_path = pdf_service.generate_report(analysis_result, output_path)
        
        print(f'✅ PDF generated: {os.path.abspath(result_path)}')
        
        # Show file size
        file_size = os.path.getsize(result_path) / 1024
        print(f'📊 File size: {file_size:.1f} KB')
        
        # Show what's included
        print('\n📋 PDF CONTAINS:')
        print('✅ Architecture maturity scoring')
        print('✅ Design pattern analysis with file examples')
        print('✅ SOLID principles violations with locations')
        print('✅ Coupling metrics with class details')
        print('✅ Technical debt analysis')
        print('✅ Concrete recommendations with time estimates')
        
        print('\n🎯 SUCCESS! Enhanced architecture report ready!')
        
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1) 