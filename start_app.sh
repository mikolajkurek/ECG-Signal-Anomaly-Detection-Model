#!/bin/bash

# ECG Signal Anomaly Detection Model - Startup Script
# This script activates the conda environment and starts the Flask application

echo "🚀 Starting ECG Signal Anomaly Detection Model..."

# Activate the conda environment
echo "🔄 Activating conda environment 'ECG-Signal-Anomaly-Detection-Model'..."
source ~/miniconda3/etc/profile.d/conda.sh 2>/dev/null || source ~/anaconda3/etc/profile.d/conda.sh 2>/dev/null || source /opt/anaconda3/etc/profile.d/conda.sh
conda activate ECG-Signal-Anomaly-Detection-Model

# Check if environment was activated successfully
if [[ "$CONDA_DEFAULT_ENV" != "ECG-Signal-Anomaly-Detection-Model" ]]; then
    echo "❌ Failed to activate conda environment. Please run 'conda activate ECG-Signal-Anomaly-Detection-Model' manually."
    exit 1
fi

echo "✅ Environment activated successfully!"

# Check if required files exist
if [ ! -f "ekg_model.keras" ]; then
    echo "❌ Model file 'ekg_model.keras' not found!"
    exit 1
fi

if [ ! -f "sample_mitbih.csv" ]; then
    echo "❌ Data file 'sample_mitbih.csv' not found!"
    exit 1
fi

echo "✅ Required files found!"

# Start the Flask application
echo "🌐 Starting Flask server on http://localhost:5001..."
python app.py
