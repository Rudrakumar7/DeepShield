import os
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

from utils.ai_engine import analyze_image
import glob

def verify_system():
    print("="*50)
    print("DEEPSHIELD FULL VERIFICATION")
    print("="*50)
    
    test_dirs = {
        'Real Samples': r'datasets\processed\val\real\*.jpg',
        'Fake Samples': r'datasets\processed\val\fake\*.jpg'
    }
    
    summary = {
        'Real Samples': {'total': 0, 'correct': 0, 'results': {}},
        'Fake Samples': {'total': 0, 'correct': 0, 'results': {}}
    }
    
    for category, pattern in test_dirs.items():
        print(f"\n[{category}]")
        files = glob.glob(pattern)
        if not files:
            print(f"  ⚠️ No files found for {pattern}")
            continue
            
        # Test 10 samples from each for a better statistical view
        target_files = files[:10]
        summary[category]['total'] = len(target_files)
        
        for filepath in target_files:
            try:
                analysis = analyze_image(filepath)
                res_type = analysis['result']
                
                is_correct = False
                if category == 'Real Samples':
                    if res_type == 'Real':
                        is_correct = True
                        summary[category]['correct'] += 1
                else: # Fake Samples
                    if res_type in ['Deepfake', 'AI Generated', 'AI Modified', 'Suspicious']:
                        is_correct = True
                        summary[category]['correct'] += 1
                
                summary[category]['results'][res_type] = summary[category]['results'].get(res_type, 0) + 1
                
                icon = "✅" if is_correct else "❌"
                print(f"  {icon} {os.path.basename(filepath)} -> {res_type} ({analysis['confidence']}%)")
            except Exception as e:
                print(f"  ❌ Error matching {filepath}: {e}")

    print("\n" + "="*50)
    print("FINAL ACCURACY REPORT")
    print("="*50)
    for cat, data in summary.items():
        acc = (data['correct'] / data['total'] * 100) if data['total'] > 0 else 0
        print(f"{cat}: {data['correct']}/{data['total']} ({acc:.1f}%)")
        print(f"  Breakdown: {data['results']}")

if __name__ == "__main__":
    verify_system()
