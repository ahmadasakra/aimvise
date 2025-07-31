import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
import tempfile
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib import colors
from PIL import Image as PILImage

logger = logging.getLogger(__name__)

class PDFService:
    """Service for generating professional PDF reports with mVISE branding"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # mVISE brand colors
        self.primary_color = HexColor('#8b5cf6')  # Purple
        self.secondary_color = HexColor('#1e293b')  # Dark blue
        self.accent_color = HexColor('#10b981')  # Green
        self.warning_color = HexColor('#f59e0b')  # Orange
        self.danger_color = HexColor('#ef4444')  # Red

    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontName='Helvetica-Bold',
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#1e293b'),
            alignment=TA_CENTER
        ))
        
        # Heading styles
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=18,
            spaceAfter=12,
            spaceBefore=20,
            textColor=HexColor('#8b5cf6')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            spaceAfter=8,
            spaceBefore=12,
            textColor=HexColor('#1e293b')
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            textColor=black
        ))
        
        # Bullet points
        self.styles.add(ParagraphStyle(
            name='CustomBullet',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            spaceAfter=4,
            leftIndent=20,
            bulletIndent=10,
            textColor=black
        ))

    def generate_report(self, analysis_result: Dict[str, Any], output_path: str = None) -> str:
        """Generate a comprehensive PDF report"""
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"mVISE_analysis_report_{timestamp}.pdf"

        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Build content
            story = []
            
            # Add title page
            story.extend(self._create_title_page(analysis_result))
            story.append(PageBreak())
            
            # Add executive summary
            story.extend(self._create_executive_summary(analysis_result))
            story.append(PageBreak())
            
            # Add technical overview
            story.extend(self._create_technical_overview(analysis_result))
            story.append(PageBreak())
            
            # Add detailed analysis sections
            story.extend(self._create_architecture_analysis(analysis_result))
            story.append(PageBreak())
            
            story.extend(self._create_technology_stack_analysis(analysis_result))
            story.append(PageBreak())
            
            story.extend(self._create_code_quality_analysis(analysis_result))
            story.append(PageBreak())
            
            story.extend(self._create_security_analysis(analysis_result))
            story.append(PageBreak())
            
            story.extend(self._create_business_impact_analysis(analysis_result))
            story.append(PageBreak())
            
            story.extend(self._create_investment_recommendations(analysis_result))
            
            # Build PDF
            
            # FINAL CONCLUSION SECTION
            final_conclusion = analysis_result.get('detailed_analysis', {}).get('comprehensive_ai_analysis', {}).get('final_conclusion', {})
            if final_conclusion:
                story.append(PageBreak())
                story.append(Paragraph("🎯 FAZIT UND EMPFEHLUNGEN", self.styles['CustomHeading1']))
                
                # Overall Assessment
                overall_assessment = final_conclusion.get('overall_assessment', '')
                if overall_assessment:
                    story.append(Paragraph("Gesamteinschätzung:", self.styles['CustomHeading2']))
                    story.append(Paragraph(overall_assessment, self.styles['CustomBody']))
                    story.append(Spacer(1, 12))
                
                # Investment Recommendation
                investment_rec = final_conclusion.get('investment_recommendation', '')
                investment_reasoning = final_conclusion.get('investment_reasoning', '')
                if investment_rec:
                    story.append(Paragraph("Investitionsempfehlung:", self.styles['CustomHeading2']))
                    
                    # Color-code the recommendation
                    rec_color = '#10b981' if 'Empfehlen' in investment_rec else '#ef4444' if 'Nicht empfehlen' in investment_rec else '#f59e0b'
                    rec_text = f"<font color='{rec_color}'><b>{investment_rec}</b></font>"
                    story.append(Paragraph(rec_text, self.styles['CustomBody']))
                    
                    if investment_reasoning:
                        story.append(Paragraph(f"<b>Begründung:</b> {investment_reasoning}", self.styles['CustomBody']))
                    story.append(Spacer(1, 12))
                
                # Top 3 Critical Improvements
                top_improvements = final_conclusion.get('top_3_critical_improvements', [])
                if top_improvements:
                    story.append(Paragraph("🚀 Top 3 Kritische Verbesserungen:", self.styles['CustomHeading2']))
                    
                    improvements_data = [['Priorität', 'Verbesserung', 'Zeitrahmen', 'Business Impact']]
                    for i, improvement in enumerate(top_improvements[:3], 1):
                        improvements_data.append([
                            str(i),
                            improvement.get('improvement', ''),
                            improvement.get('timeline', ''),
                            improvement.get('business_impact', '')
                        ])
                    
                    improvements_table = Table(improvements_data, colWidths=[0.8*inch, 2.5*inch, 1.2*inch, 2*inch])
                    improvements_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ]))
                    story.append(improvements_table)
                    story.append(Spacer(1, 12))
                
                # Long-term Roadmap
                roadmap = final_conclusion.get('long_term_roadmap', {})
                if roadmap:
                    story.append(Paragraph("📅 Langfristige Roadmap:", self.styles['CustomHeading2']))
                    
                    for period, tasks in roadmap.items():
                        if tasks:
                            period_german = {
                                'next_3_months': 'Nächste 3 Monate',
                                'next_6_months': 'Nächste 6 Monate', 
                                'next_12_months': 'Nächste 12 Monate'
                            }.get(period, period)
                            
                            story.append(Paragraph(f"<b>{period_german}:</b>", self.styles['CustomHeading3']))
                            for task in tasks[:3]:  # Show top 3 tasks per period
                                story.append(Paragraph(f"• {task}", self.styles['CustomBody']))
                            story.append(Spacer(1, 8))
                
                # Business Continuity Risk
                bc_risk = final_conclusion.get('business_continuity_risk', '')
                if bc_risk:
                    story.append(Paragraph("⚠️ Business Continuity Risiko:", self.styles['CustomHeading2']))
                    risk_color = '#ef4444' if bc_risk == 'high' else '#f59e0b' if bc_risk == 'medium' else '#10b981'
                    risk_text = f"<font color='{risk_color}'><b>{bc_risk.upper()}</b></font>"
                    story.append(Paragraph(risk_text, self.styles['CustomBody']))
                    story.append(Spacer(1, 12))
                
                # Competitive Advantage
                comp_advantage = final_conclusion.get('competitive_advantage_potential', '')
                if comp_advantage:
                    story.append(Paragraph("🏆 Wettbewerbsvorteil-Potenzial:", self.styles['CustomHeading2']))
                    story.append(Paragraph(comp_advantage, self.styles['CustomBody']))
                    story.append(Spacer(1, 12))


        doc.build(story)
        
        logger.info(f"PDF report generated: {output_path}")
        return output_path
        
    except Exception as e:
            logger.error(f"Error generating PDF report: {e}")
            raise

    def _create_title_page(self, analysis_result: Dict[str, Any]) -> List:
        """Create the title page with mVISE branding"""
        story = []
        
        # Add mVISE logo if available
        logo_path = "public/images/logo.png"
        if os.path.exists(logo_path):
            try:
                # Resize logo
                img = PILImage.open(logo_path)
                aspect = img.height / img.width
                logo_width = 2 * inch
                logo_height = logo_width * aspect
                
                logo = Image(logo_path, width=logo_width, height=logo_height)
                logo.hAlign = 'CENTER'
                story.append(logo)
                story.append(Spacer(1, 20))
            except Exception as e:
                logger.warning(f"Could not load logo: {e}")
        
        # Title
        story.append(Paragraph("AI-mVISE Repository Analyse Bericht", self.styles['CustomTitle']))
        story.append(Spacer(1, 30))
        
        # Repository info table
        repo_data = [
            ['Repository:', analysis_result.get('repository_name', 'Unbekannt')],
            ['URL:', analysis_result.get('repository_url', 'N/A')],
            ['Analyse Datum:', datetime.now().strftime('%d. %B %Y um %H:%M')],
            ['Analyse ID:', analysis_result.get('id', 'N/A')],
        ]
        
        repo_table = Table(repo_data, colWidths=[2*inch, 4*inch])
        repo_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (0, -1), self.primary_color),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        story.append(repo_table)
        story.append(Spacer(1, 40))
        
        # Overall quality score
        
        if analysis_result.get('overall_scores', {}).get('overall_quality_score'):
            score = analysis_result['overall_scores']['overall_quality_score']
            story.append(Paragraph("Gesamt-Qualitätsbewertung", self.styles['CustomHeading1']))
            
            # Quality score with visual indicator
            score_color = self._get_score_color(score)
            score_text = f"<font color='{score_color}'><b>{score}/100</b></font> - {self._get_quality_label_german(score)}"
            story.append(Paragraph(score_text, self.styles['CustomBody']))
            story.append(Spacer(1, 12))
            
            # DETAILED QUALITY BREAKDOWN - Show scoring criteria
            quality_explanation = analysis_result.get('detailed_analysis', {}).get('comprehensive_ai_analysis', {}).get('quality_scoring_explanation', {})
            if quality_explanation:
                story.append(Paragraph("📊 Detaillierte Bewertungskriterien:", self.styles['CustomHeading2']))
                
                breakdown = quality_explanation.get('overall_score_breakdown', {})
                if breakdown:
                    criteria_data = [
                        ['Kriterium', 'Punkte', 'Begründung']
                    ]
                    
                    criteria_items = [
                        ('Code-Struktur', 'code_structure_score', 'code_structure_reasoning'),
                        ('Dokumentation', 'documentation_score', 'documentation_reasoning'),
                        ('Fehlerbehandlung', 'error_handling_score', 'error_handling_reasoning'),
                        ('Performance', 'performance_score', 'performance_reasoning'),
                        ('Sicherheit', 'security_score', 'security_reasoning'),
                        ('Wartbarkeit', 'maintainability_score', 'maintainability_reasoning'),
                        ('Testing', 'testing_score', 'testing_reasoning')
                    ]
                    
                    for name, score_key, reason_key in criteria_items:
                        score_val = breakdown.get(score_key, 0)
                        reasoning = breakdown.get(reason_key, 'Keine Begründung verfügbar')
                        # Truncate long reasoning for table
                        if len(reasoning) > 100:
                            reasoning = reasoning[:97] + '...'
                        criteria_data.append([name, f"{score_val}", reasoning])
                    
                    criteria_table = Table(criteria_data, colWidths=[1.5*inch, 0.8*inch, 4*inch])
                    criteria_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ]))
                    story.append(criteria_table)
                    story.append(Spacer(1, 12))
                
                # Improvement suggestions
                improvements = quality_explanation.get('improvement_for_higher_score', [])
                if improvements:
                    story.append(Paragraph("💡 Verbesserungen für höhere Bewertung:", self.styles['CustomHeading3']))
                    for improvement in improvements[:5]:  # Show top 5
                        story.append(Paragraph(f"• {improvement}", self.styles['CustomBody']))
                    story.append(Spacer(1, 12))
        
        # Technology stack
        if analysis_result.get('ai_insights', {}).get('technology_stack'):
            tech_stack = analysis_result['ai_insights']['technology_stack']
            story.append(Paragraph("Technology Stack", self.styles['CustomHeading2']))
            
            for category, technologies in tech_stack.items():
                if technologies and isinstance(technologies, list):
                    story.append(Paragraph(f"<b>{category.title()}:</b> {', '.join(technologies)}", self.styles['CustomBody']))
            
            story.append(Spacer(1, 12))
        
        # Quality scores visualization
        if analysis_result.get('overall_scores'):
            scores = analysis_result['overall_scores']
            story.append(Paragraph("Quality Scores Overview", self.styles['CustomHeading2']))
            
            score_data = [['Metric', 'Score', 'Assessment']]
            for metric, score in scores.items():
                if isinstance(score, (int, float)):
                    label = self._get_quality_label(score)
                    score_data.append([metric.replace('_', ' ').title(), f"{score}%", label])
            
            score_table = Table(score_data, colWidths=[2.5*inch, 1*inch, 2.5*inch])
            score_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            
            story.append(score_table)
        
        return story

    def _create_architecture_analysis(self, analysis_result: Dict[str, Any]) -> List:
        """Create architecture analysis section"""
        story = []
        
        story.append(Paragraph("Architecture Analysis", self.styles['CustomHeading1']))
        
        # Get architecture data from detailed analysis
        arch_data = analysis_result.get('detailed_analysis', {}).get('comprehensive_ai_analysis', {}).get('architecture_analysis', {})
        
        if arch_data:
            # Architecture pattern
            if arch_data.get('pattern'):
                story.append(Paragraph("Architecture Pattern", self.styles['CustomHeading2']))
                story.append(Paragraph(arch_data['pattern'], self.styles['CustomBody']))
                story.append(Spacer(1, 12))
            
            # Design patterns
            if arch_data.get('design_patterns'):
                story.append(Paragraph("Design Patterns", self.styles['CustomHeading2']))
                for pattern in arch_data['design_patterns']:
                    story.append(Paragraph(f"• {pattern}", self.styles['CustomBullet']))
                story.append(Spacer(1, 12))
            
            # Scores
            scores_data = [
                ['Architecture Score', arch_data.get('architecture_score', 'N/A')],
                ['Scalability Score', arch_data.get('scalability_score', 'N/A')],
                ['Maintainability Score', arch_data.get('maintainability_score', 'N/A')],
            ]
            
            scores_table = Table(scores_data, colWidths=[3*inch, 1.5*inch])
            scores_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            
            story.append(scores_table)
        
        return story

    def _create_technology_stack_analysis(self, analysis_result: Dict[str, Any]) -> List:
        """Create technology stack analysis section"""
        story = []
        
        story.append(Paragraph("Technology Stack Analysis", self.styles['CustomHeading1']))
        
        tech_data = analysis_result.get('detailed_analysis', {}).get('comprehensive_ai_analysis', {}).get('technology_stack', {})
        
        if tech_data:
            # Frontend technologies
            if tech_data.get('frontend'):
                story.append(Paragraph("Frontend Technologies", self.styles['CustomHeading2']))
                for tech in tech_data['frontend']:
                    story.append(Paragraph(f"• {tech}", self.styles['CustomBullet']))
                story.append(Spacer(1, 12))
            
            # Backend technologies
            if tech_data.get('backend'):
                story.append(Paragraph("Backend Technologies", self.styles['CustomHeading2']))
                for tech in tech_data['backend']:
                    story.append(Paragraph(f"• {tech}", self.styles['CustomBullet']))
                story.append(Spacer(1, 12))
            
            # Database technologies
            if tech_data.get('database'):
                story.append(Paragraph("Database Technologies", self.styles['CustomHeading2']))
                for tech in tech_data['database']:
                    story.append(Paragraph(f"• {tech}", self.styles['CustomBullet']))
                story.append(Spacer(1, 12))
            
            # Build tools
            if tech_data.get('build_tools'):
                story.append(Paragraph("Build Tools", self.styles['CustomHeading2']))
                for tool in tech_data['build_tools']:
                    story.append(Paragraph(f"• {tool}", self.styles['CustomBullet']))
                story.append(Spacer(1, 12))
            
            # Outdated components
            if tech_data.get('outdated_components'):
                story.append(Paragraph("Outdated Components", self.styles['CustomHeading2']))
                for component in tech_data['outdated_components']:
                    story.append(Paragraph(f"• {component}", self.styles['CustomBullet']))
                story.append(Spacer(1, 12))
        
        return story

    def _create_code_quality_analysis(self, analysis_result: Dict[str, Any]) -> List:
        """Create code quality analysis section"""
        story = []
        
        story.append(Paragraph("Code Quality Analysis", self.styles['CustomHeading1']))
        
        quality_data = analysis_result.get('detailed_analysis', {}).get('comprehensive_ai_analysis', {}).get('code_quality', {})
        
        if quality_data:
            # Quality scores
            quality_scores = [
                ['Readability Score', quality_data.get('readability_score', 'N/A')],
                ['Maintainability Score', quality_data.get('maintainability_score', 'N/A')],
                ['Performance Score', quality_data.get('performance_score', 'N/A')],
                ['Testability Score', quality_data.get('testability_score', 'N/A')],
                ['Error Handling Score', quality_data.get('error_handling_score', 'N/A')],
                ['Overall Quality Score', quality_data.get('overall_quality_score', 'N/A')],
            ]
            
            quality_table = Table(quality_scores, colWidths=[3*inch, 1.5*inch])
            quality_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            
            story.append(quality_table)
            story.append(Spacer(1, 20))
            
            # Code smells
            if quality_data.get('code_smells'):
                story.append(Paragraph("Code Smells Identified", self.styles['CustomHeading2']))
                for smell in quality_data['code_smells']:
                    story.append(Paragraph(f"• {smell}", self.styles['CustomBullet']))
                story.append(Spacer(1, 12))
            
            # Refactoring suggestions
            if quality_data.get('refactoring_suggestions'):
                story.append(Paragraph("Refactoring Suggestions", self.styles['CustomHeading2']))
                for suggestion in quality_data['refactoring_suggestions']:
                    story.append(Paragraph(f"• {suggestion}", self.styles['CustomBullet']))
                story.append(Spacer(1, 12))
        
        return story

    def _create_security_analysis(self, analysis_result: Dict[str, Any]) -> List:
        """Create security analysis section"""
        story = []
        
        story.append(Paragraph("Security Analysis", self.styles['CustomHeading1']))
        
        security_data = analysis_result.get('detailed_analysis', {}).get('comprehensive_ai_analysis', {}).get('security_assessment', {})
        
        if security_data:
            # Security score
            score = security_data.get('security_score', 'N/A')
            risk_level = security_data.get('risk_level', 'unknown')
            
            story.append(Paragraph(f"Security Score: {score}% (Risk Level: {risk_level.title()})", self.styles['CustomBody']))
            story.append(Spacer(1, 12))
            
            # Vulnerabilities
            if security_data.get('vulnerabilities'):
                story.append(Paragraph("Vulnerabilities Found", self.styles['CustomHeading2']))
                for vuln in security_data['vulnerabilities']:
                    story.append(Paragraph(f"• {vuln}", self.styles['CustomBullet']))
                story.append(Spacer(1, 12))
            
            # Security strengths
            if security_data.get('security_strengths'):
                story.append(Paragraph("Security Strengths", self.styles['CustomHeading2']))
                for strength in security_data['security_strengths']:
                    story.append(Paragraph(f"• {strength}", self.styles['CustomBullet']))
                story.append(Spacer(1, 12))
            
            # Security recommendations
            if security_data.get('recommendations'):
                story.append(Paragraph("Security Recommendations", self.styles['CustomHeading2']))
                for rec in security_data['recommendations']:
                    story.append(Paragraph(f"• {rec}", self.styles['CustomBullet']))
                story.append(Spacer(1, 12))
        
        return story

    def _create_business_impact_analysis(self, analysis_result: Dict[str, Any]) -> List:
        """Create business impact analysis section"""
        story = []
        
        story.append(Paragraph("Business Impact Analysis", self.styles['CustomHeading1']))
        
        business_data = analysis_result.get('business_impact', {})
        
        if business_data:
            # Key metrics
            impact_data = [
                ['Technical Debt (Hours)', business_data.get('technical_debt_hours', 'N/A')],
                ['Development Velocity', business_data.get('development_velocity', 'N/A').title()],
                ['Risk Level', business_data.get('risk_level', 'N/A').title()],
                ['Maintenance Cost', business_data.get('maintenance_cost_estimate', 'N/A')],
                ['Scalability Potential', business_data.get('scalability_potential', 'N/A')],
            ]
            
            impact_table = Table(impact_data, colWidths=[3*inch, 2*inch])
            impact_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            
            story.append(impact_table)
            story.append(Spacer(1, 20))
            
            # ROI opportunities
            if business_data.get('roi_opportunities'):
                story.append(Paragraph("ROI Opportunities", self.styles['CustomHeading2']))
                for opportunity in business_data['roi_opportunities']:
                    story.append(Paragraph(f"• {opportunity}", self.styles['CustomBullet']))
                story.append(Spacer(1, 12))
        
        return story

    def _create_investment_recommendations(self, analysis_result: Dict[str, Any]) -> List:
        """Create investment recommendations section"""
        story = []
        
        story.append(Paragraph("Investment Recommendations", self.styles['CustomHeading1']))
        
        recommendations = analysis_result.get('investment_recommendations', [])
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                story.append(Paragraph(f"Priority {rec.get('priority', i)}: {rec.get('task', 'Unknown Task')}", self.styles['CustomHeading2']))
                
                rec_data = [
                    ['Effort (Hours)', rec.get('effort_hours', 'N/A')],
                    ['Business Value', rec.get('business_value', 'N/A').title()],
                    ['Description', rec.get('description', 'N/A')],
                    ['Expected ROI', rec.get('expected_roi', 'N/A')],
                    ['Risk if Not Done', rec.get('risk_if_not_done', 'N/A')],
                ]
                
                rec_table = Table(rec_data, colWidths=[2*inch, 4*inch])
                rec_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.lightgrey]),
                ]))
                
                story.append(rec_table)
                story.append(Spacer(1, 15))
        
        return story

    def _get_score_color(self, score: int) -> str:
        """Get color based on score"""
        if score >= 90:
            return '#10b981'  # Green
        elif score >= 80:
            return '#f59e0b'  # Orange
        elif score >= 70:
            return '#f97316'  # Orange
        else:
            return '#ef4444'  # Red

    def _get_quality_label(self, score: int) -> str:
        """Get quality label based on score"""
        if score >= 90:
            return 'Excellent'
        elif score >= 80:
            return 'Good'
        elif score >= 70:
            return 'Fair'
        else:
            return 'Needs Improvement'
    

    def _get_score_color(self, score: int) -> str:
        """Get color based on score"""
        if score >= 90:
            return '#10b981'  # Green
        elif score >= 80:
            return '#8b5cf6'  # Purple
        elif score >= 70:
            return '#f59e0b'  # Orange
        else:
            return '#ef4444'  # Red

    def _get_quality_label_german(self, score: int) -> str:
        """Get German quality label based on score"""
        if score >= 90:
            return 'Ausgezeichnet'
        elif score >= 80:
            return 'Gut'
        elif score >= 70:
            return 'Befriedigend'
        else:
            return 'Verbesserungsbedürftig' 