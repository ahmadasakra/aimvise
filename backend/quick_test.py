#!/usr/bin/env python3
"""Quick test of architecture analyzer"""

from pathlib import Path
from app.services.analyzers.architecture_analyzer import ArchitectureAnalyzer

def test_analyzer():
    print("🔬 Quick Architecture Analyzer Test")
    print("=" * 50)
    
    try:
        # Test with current directory
        repo_path = Path('.')
        analyzer = ArchitectureAnalyzer(repo_path)
        
        print("📁 Running analysis...")
        results = analyzer.analyze()
        
        # Check if we got results
        if 'architecture_maturity' in results:
            maturity = results['architecture_maturity']
            score = maturity.get('overall_score', 0)
            level = maturity.get('level', 'Unknown')
            
            print(f"✅ Analysis successful!")
            print(f"📊 Score: {score:.1f}/10")
            print(f"📈 Level: {level}")
            
            # Check breakdown
            breakdown = maturity.get('breakdown', {})
            print("\n📋 Breakdown:")
            for category, score in breakdown.items():
                print(f"  • {category}: {score:.1f}/10")
            
            return True
        else:
            print("❌ No architecture_maturity in results")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_analyzer()
    exit(0 if success else 1) 