"""
Comprehensive Pre-Deployment Test Script for Oracle Samuel
Tests all modules, dependencies, and functionality before Streamlit Cloud deployment
"""

import sys
import os
from datetime import datetime

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("=" * 80)
print("ORACLE SAMUEL - PRE-DEPLOYMENT TEST SUITE")
print("=" * 80)
print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Test results
test_results = {
    'passed': [],
    'failed': [],
    'warnings': []
}

def test_result(test_name, passed, message=""):
    """Record test result"""
    if passed:
        test_results['passed'].append(test_name)
        print(f"[PASS] {test_name}")
    else:
        test_results['failed'].append(test_name)
        print(f"[FAIL] {test_name}")
    if message:
        print(f"   {message}")
    print()

# =============================================================================
# TEST 1: Core Dependencies
# =============================================================================
print("TEST 1: Core Dependencies")
print("-" * 80)

try:
    import streamlit as st
    test_result("Import streamlit", True, f"Version: {st.__version__}")
except Exception as e:
    test_result("Import streamlit", False, str(e))

try:
    import pandas as pd
    test_result("Import pandas", True, f"Version: {pd.__version__}")
except Exception as e:
    test_result("Import pandas", False, str(e))

try:
    import numpy as np
    test_result("Import numpy", True, f"Version: {np.__version__}")
except Exception as e:
    test_result("Import numpy", False, str(e))

try:
    from sklearn.cluster import KMeans
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
    from sklearn.preprocessing import StandardScaler
    import sklearn
    test_result("Import scikit-learn", True, f"Version: {sklearn.__version__}")
except Exception as e:
    test_result("Import scikit-learn", False, str(e))

try:
    import matplotlib
    test_result("Import matplotlib", True, f"Version: {matplotlib.__version__}")
except Exception as e:
    test_result("Import matplotlib", False, str(e))

try:
    import seaborn as sns
    test_result("Import seaborn", True, f"Version: {sns.__version__}")
except Exception as e:
    test_result("Import seaborn", False, str(e))

try:
    import plotly
    test_result("Import plotly", True, f"Version: {plotly.__version__}")
except Exception as e:
    test_result("Import plotly", False, str(e))

# =============================================================================
# TEST 2: Advanced ML Libraries
# =============================================================================
print("TEST 2: Advanced ML Libraries")
print("-" * 80)

try:
    import xgboost as xgb
    test_result("Import xgboost", True, f"Version: {xgb.__version__}")
except Exception as e:
    test_result("Import xgboost", False, str(e))

try:
    import lightgbm as lgb
    test_result("Import lightgbm", True, f"Version: {lgb.__version__}")
except Exception as e:
    test_result("Import lightgbm", False, str(e))

try:
    import catboost
    test_result("Import catboost", True, f"Version: {catboost.__version__}")
except Exception as e:
    test_result("Import catboost", False, str(e))

try:
    from prophet import Prophet
    test_result("Import prophet", True)
except Exception as e:
    test_result("Import prophet", False, str(e))

try:
    import optuna
    test_result("Import optuna", True, f"Version: {optuna.__version__}")
except Exception as e:
    test_result("Import optuna", False, str(e))

# =============================================================================
# TEST 3: Explainability Libraries
# =============================================================================
print("TEST 3: Explainability Libraries")
print("-" * 80)

try:
    import shap
    test_result("Import shap", True, f"Version: {shap.__version__}")
except Exception as e:
    test_result("Import shap", False, str(e))

try:
    import lime
    test_result("Import lime", True)
except Exception as e:
    test_result("Import lime", False, str(e))

# =============================================================================
# TEST 4: Geo and Mapping Libraries
# =============================================================================
print("TEST 4: Geo and Mapping Libraries")
print("-" * 80)

try:
    import folium
    test_result("Import folium", True, f"Version: {folium.__version__}")
except Exception as e:
    test_result("Import folium", False, str(e))

try:
    import geopy
    test_result("Import geopy", True, f"Version: {geopy.__version__}")
except Exception as e:
    test_result("Import geopy", False, str(e))

try:
    import pydeck
    test_result("Import pydeck", True, f"Version: {pydeck.__version__}")
except Exception as e:
    test_result("Import pydeck", False, str(e))

# =============================================================================
# TEST 5: Voice and Image Processing
# =============================================================================
print("TEST 5: Voice and Image Processing")
print("-" * 80)

try:
    from gtts import gTTS
    test_result("Import gtts", True)
except Exception as e:
    test_result("Import gtts", False, str(e))

try:
    import speech_recognition as sr
    test_result("Import speech_recognition", True, f"Version: {sr.__version__}")
except Exception as e:
    test_result("Import speech_recognition", False, str(e))

try:
    from PIL import Image
    import PIL
    test_result("Import Pillow", True, f"Version: {PIL.__version__}")
except Exception as e:
    test_result("Import Pillow", False, str(e))

try:
    import cv2
    test_result("Import opencv-python", True, f"Version: {cv2.__version__}")
except Exception as e:
    test_result("Import opencv-python", False, str(e))

# =============================================================================
# TEST 6: Custom Modules
# =============================================================================
print("TEST 6: Custom Modules")
print("-" * 80)

try:
    from utils.md5_manager import generate_md5_from_dataframe, create_signature_record
    test_result("Import utils.md5_manager", True)
except Exception as e:
    test_result("Import utils.md5_manager", False, str(e))

try:
    from utils.database_manager import DatabaseManager
    test_result("Import utils.database_manager", True)
except Exception as e:
    test_result("Import utils.database_manager", False, str(e))

try:
    from flowing_background import apply_flowing_background, flowing_header, flowing_card, flowing_metric
    test_result("Import flowing_background", True)
except Exception as e:
    test_result("Import flowing_background", False, str(e))

try:
    from utils.data_cleaner import DataCleaner
    test_result("Import utils.data_cleaner", True)
except Exception as e:
    test_result("Import utils.data_cleaner", False, str(e))

try:
    from utils.predictor import RealEstatePredictor
    test_result("Import utils.predictor", True)
except Exception as e:
    test_result("Import utils.predictor", False, str(e))

try:
    from utils.visualizer import RealEstateVisualizer
    test_result("Import utils.visualizer", True)
except Exception as e:
    test_result("Import utils.visualizer", False, str(e))

try:
    from agent import OracleSamuelAgent
    test_result("Import agent", True)
except Exception as e:
    test_result("Import agent", False, str(e))

# =============================================================================
# TEST 7: Self-Learning Modules
# =============================================================================
print("TEST 7: Self-Learning Modules")
print("-" * 80)

try:
    from self_learning.trainer import SelfLearningTrainer
    test_result("Import self_learning.trainer", True)
except Exception as e:
    test_result("Import self_learning.trainer", False, str(e))

try:
    from self_learning.evaluator import ModelEvaluator
    test_result("Import self_learning.evaluator", True)
except Exception as e:
    test_result("Import self_learning.evaluator", False, str(e))

try:
    from self_learning.retrain_manager import RetrainManager
    test_result("Import self_learning.retrain_manager", True)
except Exception as e:
    test_result("Import self_learning.retrain_manager", False, str(e))

try:
    from self_learning.feedback_manager import FeedbackManager
    test_result("Import self_learning.feedback_manager", True)
except Exception as e:
    test_result("Import self_learning.feedback_manager", False, str(e))

try:
    from self_learning.knowledge_base import KnowledgeBase
    test_result("Import self_learning.knowledge_base", True)
except Exception as e:
    test_result("Import self_learning.knowledge_base", False, str(e))

# =============================================================================
# TEST 8: Voice, Vision, and Geo Modules
# =============================================================================
print("TEST 8: Voice, Vision, and Geo Modules")
print("-" * 80)

try:
    from voice_agent.voice_handler import VoiceHandler
    test_result("Import voice_agent.voice_handler", True)
except Exception as e:
    test_result("Import voice_agent.voice_handler", False, str(e))

try:
    from voice_agent.tts_manager import TTSManager
    test_result("Import voice_agent.tts_manager", True)
except Exception as e:
    test_result("Import voice_agent.tts_manager", False, str(e))

try:
    from vision.image_analyzer import PropertyImageAnalyzer
    test_result("Import vision.image_analyzer", True)
except Exception as e:
    test_result("Import vision.image_analyzer", False, str(e))

try:
    from vision.detector_utils import PropertyFeatureDetector
    test_result("Import vision.detector_utils", True)
except Exception as e:
    test_result("Import vision.detector_utils", False, str(e))

try:
    from geo.map_visualizer import RealEstateMapVisualizer
    test_result("Import geo.map_visualizer", True)
except Exception as e:
    test_result("Import geo.map_visualizer", False, str(e))

try:
    from geo.geo_forecast import GeoForecastEngine
    test_result("Import geo.geo_forecast", True)
except Exception as e:
    test_result("Import geo.geo_forecast", False, str(e))

try:
    from utils.integrity_checker import ProjectIntegrityChecker
    test_result("Import utils.integrity_checker", True)
except Exception as e:
    test_result("Import utils.integrity_checker", False, str(e))

# =============================================================================
# TEST 9: File Structure
# =============================================================================
print("TEST 9: File Structure")
print("-" * 80)

required_files = [
    'app.py',
    'requirements.txt',
    '.gitignore',
    'utils/md5_manager.py',
    'utils/database_manager.py',
    'utils/data_cleaner.py',
    'utils/predictor.py',
    'utils/visualizer.py',
    'flowing_background.py',
    'agent.py'
]

for file_path in required_files:
    if os.path.exists(file_path):
        test_result(f"File exists: {file_path}", True)
    else:
        test_result(f"File exists: {file_path}", False, "File not found!")

# =============================================================================
# TEST 10: Database Functionality
# =============================================================================
print("TEST 10: Database Functionality")
print("-" * 80)

try:
    from utils.database_manager import DatabaseManager
    db = DatabaseManager()
    test_result("Initialize DatabaseManager", True)
except Exception as e:
    test_result("Initialize DatabaseManager", False, str(e))

# =============================================================================
# TEST 11: Data Processing Test
# =============================================================================
print("TEST 11: Data Processing Test")
print("-" * 80)

try:
    import pandas as pd
    import numpy as np

    # Create sample data
    sample_data = pd.DataFrame({
        'price': np.random.randint(100000, 1000000, 100),
        'sqft': np.random.randint(500, 5000, 100),
        'bedrooms': np.random.randint(1, 6, 100),
        'bathrooms': np.random.randint(1, 4, 100),
        'lat': np.random.uniform(32.0, 34.0, 100),
        'lon': np.random.uniform(-118.0, -117.0, 100)
    })

    test_result("Create sample DataFrame", True, f"Shape: {sample_data.shape}")

    # Test DataCleaner
    from utils.data_cleaner import DataCleaner
    cleaner = DataCleaner(sample_data)
    cleaned_data, report = cleaner.clean_data()
    test_result("DataCleaner.clean_data()", True, f"Cleaned shape: {cleaned_data.shape}")

except Exception as e:
    test_result("Data Processing Test", False, str(e))

# =============================================================================
# FINAL SUMMARY
# =============================================================================
print("=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print(f"Tests Passed: {len(test_results['passed'])}")
print(f"Tests Failed: {len(test_results['failed'])}")
print(f"Warnings: {len(test_results['warnings'])}")
print()

if test_results['failed']:
    print("FAILED TESTS:")
    for test in test_results['failed']:
        print(f"  - {test}")
    print()
    print("[FAIL] DEPLOYMENT NOT READY - Please fix the failed tests above")
    sys.exit(1)
else:
    print("[PASS] ALL TESTS PASSED - Ready for Streamlit Cloud deployment!")
    print()
    print("DEPLOYMENT CHECKLIST:")
    print("  [PASS] All dependencies installed")
    print("  [PASS] All custom modules importable")
    print("  [PASS] File structure verified")
    print("  [PASS] Data processing functional")
    print()
    print("NEXT STEPS:")
    print("  1. Run: streamlit run app.py (to test locally)")
    print("  2. Commit and push to GitHub")
    print("  3. Deploy to Streamlit Cloud")
    sys.exit(0)
