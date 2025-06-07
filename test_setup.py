#!/usr/bin/env python3
"""
Test script to verify the ECG application components work correctly
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    try:
        import flask
        import tensorflow as tf
        import pandas as pd
        import numpy as np
        import sklearn
        print("✅ All required packages imported successfully")
        print(f"   - Flask: {flask.__version__}")
        print(f"   - TensorFlow: {tf.__version__}")
        print(f"   - Pandas: {pd.__version__}")
        print(f"   - NumPy: {np.__version__}")
        print(f"   - Scikit-learn: {sklearn.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_files():
    """Test if required files exist"""
    required_files = [
        'ekg_model.keras',
        'sample_mitbih.csv',
        'app.py',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    return all_exist

def test_model_loading():
    """Test if the model can be loaded"""
    try:
        import tensorflow as tf
        model = tf.keras.models.load_model('ekg_model.keras')
        print("✅ Model loaded successfully")
        print(f"   - Model input shape: {model.input_shape}")
        print(f"   - Model output shape: {model.output_shape}")
        return True
    except Exception as e:
        print(f"❌ Model loading error: {e}")
        return False

def test_data_loading():
    """Test if the data can be loaded"""
    try:
        import pandas as pd
        data = pd.read_csv('sample_mitbih.csv', header=None)
        print(f"✅ Data loaded successfully")
        print(f"   - Data shape: {data.shape}")
        print(f"   - Labels distribution: {data.iloc[:, -1].value_counts().to_dict()}")
        return True
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        return False

def main():
    """Run all tests"""
    print("🔬 Testing ECG Application Components...")
    print("=" * 50)
    
    tests = [
        ('Package Imports', test_imports),
        ('Required Files', test_files),
        ('Model Loading', test_model_loading),
        ('Data Loading', test_data_loading)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}:")
        result = test_func()
        results.append(result)
    
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    all_passed = all(results)
    if all_passed:
        print("🎉 All tests passed! The application is ready to run.")
        print("\nTo start the application:")
        print("1. conda activate ECG-Signal-Anomaly-Detection-Model")
        print("2. python app.py")
        print("3. Open http://localhost:5001 in your browser")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
