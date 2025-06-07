from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import json

app = Flask(__name__)

# Global variables to store data and model
data = None
model = None
scaler = None
current_row = 0

def load_data():
    """Load and prepare the ECG data"""
    global data, scaler
    try:
        # Read the balanced sample dataset (100 rows with equal distribution)
        data = pd.read_csv('sample_mitbih.csv', header=None)
        print(f"Loaded {len(data)} rows of balanced ECG sample data")
        
        # Add column names for easier handling
        feature_cols = [f'feature_{i}' for i in range(data.shape[1] - 1)]
        data.columns = feature_cols + ['label']
        
        # Initialize scaler (same as used in training)
        scaler = MinMaxScaler()
        X = data.iloc[:, :-1].values  # Signal data
        X = X.reshape(X.shape[0], X.shape[1], 1)
        scaler.fit(X.reshape(-1, X.shape[-1]))
        
        # Print label distribution
        label_counts = data['label'].value_counts().sort_index()
        print("Label distribution:")
        for label, count in label_counts.items():
            label_type = "Normal" if label == 0.0 else "Abnormal"
            print(f"  Label {label} ({label_type}): {count} samples")
        
        return True
    except Exception as e:
        print(f"Error loading data: {e}")
        return False

def load_model():
    """Load the trained model"""
    global model
    try:
        model = tf.keras.models.load_model('ekg_model.keras')
        print("Model loaded successfully")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def predict_signal(signal_data):
    """Make prediction on ECG signal"""
    global model, scaler
    if model is None or scaler is None:
        return None
    
    try:
        # Prepare signal for prediction
        signal = np.array(signal_data).reshape(1, -1, 1)
        signal_scaled = scaler.transform(signal.reshape(-1, signal.shape[-1])).reshape(signal.shape)
        
        # Make prediction
        prediction = model.predict(signal_scaled, verbose=0)[0][0]
        
        # Convert to class (0 = Normal, 1 = Abnormal)
        predicted_class = 1 if prediction > 0.5 else 0
        confidence = prediction if predicted_class == 1 else (1 - prediction)
        
        return {
            'prediction': predicted_class,
            'confidence': float(confidence),
            'raw_score': float(prediction),
            'class_name': 'Abnormal' if predicted_class == 1 else 'Normal'
        }
    except Exception as e:
        print(f"Error making prediction: {e}")
        return None

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/data/<int:row_index>')
def get_data(row_index):
    """Get ECG data for specific row"""
    global data
    if data is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    if row_index < 0 or row_index >= len(data):
        return jsonify({'error': 'Row index out of range'}), 400
    
    # Get the signal data (all columns except the last one which is the label)
    signal_data = data.iloc[row_index, :-1].tolist()
    actual_label = int(data.iloc[row_index, -1])
    
    # Make prediction
    prediction_result = predict_signal(signal_data)
    
    return jsonify({
        'row_index': row_index,
        'signal_data': signal_data,
        'actual_label': actual_label,
        'actual_class': 'Abnormal' if actual_label > 0 else 'Normal',
        'prediction': prediction_result,
        'total_rows': len(data)
    })

@app.route('/api/info')
def get_info():
    """Get dataset information"""
    global data
    if data is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    return jsonify({
        'total_rows': len(data),
        'signal_length': len(data.columns) - 1,
        'class_distribution': data.iloc[:, -1].value_counts().to_dict()
    })

@app.route('/api/filter/<filter_type>')
def get_filtered_indices(filter_type):
    """Get indices of samples matching the filter criteria"""
    global data
    if data is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    if filter_type == 'all':
        # Return all indices
        indices = list(range(len(data)))
    elif filter_type == 'normal':
        # Return indices where label is 0 (normal)
        indices = data[abs(data['label'] - 0.0) < 0.001].index.tolist()
    elif filter_type == 'abnormal':
        # Return indices where label is not 0 (abnormal)
        indices = data[abs(data['label'] - 0.0) >= 0.001].index.tolist()
    else:
        return jsonify({'error': 'Invalid filter type. Use: all, normal, abnormal'}), 400
    
    return jsonify({
        'filter_type': filter_type,
        'indices': indices,
        'count': len(indices),
        'total_rows': len(data)
    })

@app.route('/api/data/filtered/<filter_type>/<int:filtered_index>')
def get_filtered_data(filter_type, filtered_index):
    """Get ECG data for specific filtered index"""
    global data
    if data is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    # Get filtered indices
    if filter_type == 'all':
        indices = list(range(len(data)))
    elif filter_type == 'normal':
        indices = data[abs(data['label'] - 0.0) < 0.001].index.tolist()
    elif filter_type == 'abnormal':
        indices = data[abs(data['label'] - 0.0) >= 0.001].index.tolist()
    else:
        return jsonify({'error': 'Invalid filter type'}), 400
    
    if filtered_index < 0 or filtered_index >= len(indices):
        return jsonify({'error': 'Filtered index out of range'}), 400
    
    # Get actual row index
    row_index = indices[filtered_index]
    
    # Get the signal data
    signal_data = data.iloc[row_index, :-1].tolist()
    actual_label = float(data.iloc[row_index, -1])
    
    # Determine label categories
    is_normal = abs(actual_label - 0.0) < 0.001
    actual_class = 'Normal' if is_normal else 'Abnormal'
    
    # Make prediction
    prediction_result = predict_signal(signal_data)
    
    return jsonify({
        'row_index': row_index,
        'filtered_index': filtered_index,
        'filter_type': filter_type,
        'signal_data': signal_data,
        'actual_label': actual_label,
        'actual_class': actual_class,
        'prediction': prediction_result,
        'total_filtered': len(indices),
        'total_rows': len(data)
    })

if __name__ == '__main__':
    print("Loading data and model...")
    
    if not load_data():
        print("Failed to load data")
        exit(1)
    
    if not load_model():
        print("Failed to load model")
        exit(1)
    
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5001)
