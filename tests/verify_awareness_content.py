import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from utils.awareness_content import AWARENESS_TOPICS, CASE_STUDIES, GLOSSARY, DAILY_TIPS, CHECKLIST_ITEMS, MYTHS_FACTS
    print("Import Successful!")
    print(f"Topics: {len(AWARENESS_TOPICS)}")
    print(f"Cases: {len(CASE_STUDIES)}")
    print(f"Glossary: {len(GLOSSARY)}")
    print(f"Tips: {len(DAILY_TIPS)}")
    print(f"Checklist: {len(CHECKLIST_ITEMS)}")
    print(f"Myths: {len(MYTHS_FACTS)}")
    
    # Check structure of first topic
    t = AWARENESS_TOPICS[0]
    if 'id' in t and 'title' in t and 'icon' in t:
        print("Topic structure valid.")
    else:
        print("Topic structure INVALID.")

except ImportError as e:
    print(f"Import Failed: {e}")
except Exception as e:
    print(f"Error: {e}")
