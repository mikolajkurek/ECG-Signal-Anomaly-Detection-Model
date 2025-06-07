#!/bin/bash

# ECG Signal Anomaly Detection Model - Environment Setup Script
# This script sets up the conda environment and installs required packages

echo "🔧 Setting up ECG Signal Anomaly Detection Model Environment..."

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "❌ Conda is not installed. Please install Anaconda or Miniconda first."
    exit 1
fi

# Initialize conda for shell (if not already done)
conda init zsh 2>/dev/null || conda init bash 2>/dev/null

# Source conda
source ~/anaconda3/etc/profile.d/conda.sh 2>/dev/null || source ~/miniconda3/etc/profile.d/conda.sh 2>/dev/null || source /opt/anaconda3/etc/profile.d/conda.sh

# Check if environment already exists
if conda env list | grep -q "ECG-Signal-Anomaly-Detection-Model"; then
    echo "🔄 Environment 'ECG-Signal-Anomaly-Detection-Model' already exists."
    echo "🗑️  Removing existing environment to ensure clean setup..."
    conda env remove -n ECG-Signal-Anomaly-Detection-Model -y
fi

echo "🆕 Creating new conda environment from environment.yml..."
conda env create -f environment.yml

echo "🔄 Activating environment..."
conda activate ECG-Signal-Anomaly-Detection-Model

# Install additional packages with conda where possible
echo "📦 Installing additional packages with conda..."
conda install -c conda-forge matplotlib -y

# Verify installation
echo "✅ Verifying installation..."
python -c "
import flask, tensorflow, pandas, numpy, sklearn, matplotlib
print('✅ All packages imported successfully!')
print(f'   - Flask: {flask.__version__}')
print(f'   - TensorFlow: {tensorflow.__version__}')
print(f'   - Pandas: {pandas.__version__}')
print(f'   - NumPy: {numpy.__version__}')
print(f'   - Scikit-learn: {sklearn.__version__}')
print(f'   - Matplotlib: {matplotlib.__version__}')
"

echo "🎉 Setup complete! Environment is ready."
echo ""
echo "To activate the environment in the future, run:"
echo "conda activate ECG-Signal-Anomaly-Detection-Model"
echo ""
echo "To test the setup, run:"
echo "./test_setup.py"
echo ""
echo "To start the application, run:"
echo "./start_app.sh"
