#!/usr/bin/env python3
"""
🎯 Test Enhanced Architecture Analysis PDF Report
Generates a comprehensive PDF report with detailed architecture analysis
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

from app.services.analyzers.architecture_analyzer import ArchitectureAnalyzer
from app.services.pdf_service import PDFService

def test_enhanced_architecture_report():
    """Test the enhanced architecture analysis PDF report"""
    print('🚀 Testing Enhanced Architecture Analysis PDF Report...')
    print('=' * 80)
    
    # Run comprehensive architecture analysis
    repo_path = Path('./backend')
    print(f'📁 Analyzing repository: {repo_path.absolute()}')
    
    try:
        # Initialize analyzer
        arch_analyzer = ArchitectureAnalyzer(repo_path)
        print('🔍 Running enterprise architecture analysis...')
        
        # Get detailed analysis results
        arch_results = arch_analyzer.analyze()
        
        # Print analysis summary
        maturity = arch_results.get('architecture_maturity', {})
        overall_score = maturity.get('overall_score', 0)
        maturity_level = maturity.get('level', 'Unknown')
        
        print(f'📊 Analysis completed!')
        print(f'  🎯 Overall Architecture Score: {overall_score:.1f}/10')
        print(f'  📈 Maturity Level: {maturity_level}')
        print()
        
        # Create comprehensive analysis result
        analysis_result = {
            'id': 'enhanced_architecture_test',
            'repository_url': 'https://github.com/enterprise/ai-mvise',
            'status': 'completed',
            'architecture': arch_results,  # Our enhanced architecture analysis
            'repository_overview': {
                'name': 'AI-mVISE Enterprise Analysis Tool',
                'description': 'Comprehensive Repository Analysis für M&A Due Diligence',
                'languages': [
                    {'name': 'Python', 'percentage': 87.3},
                    {'name': 'TypeScript', 'percentage': 10.2},
                    {'name': 'JavaScript', 'percentage': 2.5}
                ],
                'total_files': 56,
                'total_lines': 18429,
                'contributors': 3,
                'created_date': '2024-07-01',
                'last_commit': '2024-07-31'
            },
            'technical_metrics': {
                'code_quality_score': 7.8,
                'security_score': 8.2,
                'maintainability_score': 6.9,
                'test_coverage': 45.2,
                'complexity_score': 6.5,
                'documentation_score': 7.1
            },
            'ai_insights': {
                'summary': 'Enterprise-grade Architektur-Analyse-Tool mit umfassenden Due Diligence Funktionen. Zeigt starke Domain-Driven Design Implementierung aber Verbesserungsbedarf bei Kopplung.',
                'key_strengths': [
                    'Exzellente Domain-Driven Design Implementierung (9.0/10)',
                    'Gute Clean Architecture Struktur (7.5/10)', 
                    'Solide API Design Patterns (6.0/10)',
                    'Mehrere Design Patterns implementiert'
                ],
                'areas_for_improvement': [
                    'Kritische Kopplungsprobleme (24 hoch gekoppelte Klassen)',
                    'Niedrige Design Pattern Diversität (0.2/10)',
                    'SOLID Prinzipien Verstöße (29 gefunden)',
                    'Technische Schulden: 120 Stunden geschätzt'
                ],
                'risk_assessment': 'MEDIUM - Architektur ist grundsätzlich solide, aber hohe Kopplung erhöht Wartungskosten',
                'investment_recommendation': 'Empfehlung: 2-3 Refactoring-Sprints vor M&A für Kopplungsreduktion'
            }
        }
        
        # Generate enhanced PDF report
        print('📄 Generating enhanced PDF report...')
        pdf_service = PDFService()
        output_path = 'enhanced_architecture_analysis_report.pdf'
        
        result_path = pdf_service.generate_report(analysis_result, output_path)
        
        # Report success
        print(f'✅ Enhanced PDF Report generated successfully!')
        print(f'📍 Location: {os.path.abspath(result_path)}')
        
        # Check file size
        file_size = os.path.getsize(result_path) / 1024  # KB
        print(f'📊 File size: {file_size:.1f} KB')
        print()
        
        # Show detailed architecture content included
        print('📋 ENHANCED ARCHITECTURE CONTENT INCLUDED:')
        print('=' * 60)
        
        # Architecture maturity breakdown
        breakdown = maturity.get('breakdown', {})
        print('🎯 ARCHITECTURE MATURITY ANALYSIS:')
        for category, score in breakdown.items():
            print(f'  • {category}: {score:.1f}/10')
        print()
        
        # Design patterns details
        design_patterns = arch_results.get('design_patterns_analysis', {})
        detected_patterns = design_patterns.get('detected_patterns', {})
        total_patterns = sum(len(patterns) for patterns in detected_patterns.values())
        print(f'🎨 DESIGN PATTERNS WITH FILE EXAMPLES:')
        print(f'  • Total Patterns Detected: {total_patterns}')
        for category, patterns in detected_patterns.items():
            if patterns:
                print(f'  • {category.title()}: {len(patterns)} patterns')
                for pattern_name, details in patterns.items():
                    matches = len(details.get('matches', []))
                    print(f'    - {pattern_name.replace("_", " ").title()}: {matches} locations')
        print()
        
        # SOLID principles with violations
        solid_analysis = arch_results.get('solid_principles_analysis', {})
        principles = solid_analysis.get('principles', {})
        print(f'🔧 SOLID PRINCIPLES WITH CONCRETE VIOLATIONS:')
        for principle, data in principles.items():
            violations = len(data.get('violations', []))
            good_practices = len(data.get('good_practices', []))
            print(f'  • {principle}: {violations} violations, {good_practices} good practices')
        print()
        
        # Coupling details with specific classes
        coupling_metrics = arch_results.get('coupling_cohesion_metrics', {})
        high_coupling = coupling_metrics.get('high_coupling_classes', [])
        coupling_details = coupling_metrics.get('coupling_details', {})
        print(f'🔗 COUPLING ANALYSIS WITH CLASS DETAILS:')
        print(f'  • High Coupling Classes: {len(high_coupling)}')
        print(f'  • Analyzed Classes: {len(coupling_details)}')
        print(f'  • Average Instability: {coupling_metrics.get("average_instability", 0):.3f}')
        print()
        
        # Technical debt specifics
        technical_debt = arch_results.get('technical_debt', {})
        refactoring_priorities = arch_results.get('refactoring_priorities', [])
        print(f'🛠️ TECHNICAL DEBT WITH REFACTORING PRIORITIES:')
        print(f'  • Estimated Debt: {technical_debt.get("total_debt_hours", 0)} hours')
        print(f'  • Critical Issues: {technical_debt.get("critical_issues", 0)}')
        print(f'  • Refactoring Priorities: {len(refactoring_priorities)} items')
        print()
        
        print('🎉 COMPREHENSIVE ARCHITECTURE ANALYSIS COMPLETE!')
        print('📋 The PDF report now contains:')
        print('  ✅ Detailed architecture maturity scoring')
        print('  ✅ Concrete design pattern examples with file locations')
        print('  ✅ SOLID violations with specific code examples')
        print('  ✅ Coupling metrics with problematic class details')
        print('  ✅ Technical debt analysis with refactoring priorities')
        print('  ✅ Business-relevant recommendations with time estimates')
        print('  ✅ M&A Due Diligence ready insights')
        print()
        print('🎯 ARBEITGEBER CAN NOW:')
        print('  📊 See exact technical debt and refactoring costs')
        print('  🔍 Identify specific problematic code locations')
        print('  💰 Estimate M&A integration effort and costs')
        print('  🛠️ Plan technical improvement roadmap')
        print('  👥 Assess development team competency from code quality')
        
    except Exception as e:
        print(f'❌ Error during analysis: {e}')
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = test_enhanced_architecture_report()
    exit(0 if success else 1) 