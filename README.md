# ECG Signal Anomaly Detection Model

A Flask-based web application for detecting anomalies in ECG (Electrocardiogram) signals using a trained neural network model. The application provides an interactive interface to visualize ECG data and make real-time predictions.

## 🚀 Features

- **Interactive ECG Visualization**: Real-time plotting of ECG signals
- **Anomaly Detection**: AI-powered detection using a trained neural network
- **Dataset Filtering**: Filter ECG samples by normal/abnormal classifications
- **Real-time Predictions**: Get instant predictions with confidence scores
- **Modern Web Interface**: Clean, responsive UI for easy navigation

## 📋 Prerequisites

- **Anaconda or Miniconda**: Required for environment management
- **Python 3.9+**: Compatible Python version
- **macOS/Linux/Windows**: Cross-platform compatibility

## 🛠️ Installation & Setup

### 1. Clone or Download the Project

Ensure you have all the project files in your working directory:
```
ECG-Signal-Anomaly-Detection-Model/
├── app.py                    # Main Flask application
├── ekg_model.keras          # Trained neural network model
├── sample_mitbih.csv        # ECG dataset
├── ecg_sampler.py           # Data sampling utilities
├── main.ipynb               # Jupyter notebook for model training
├── requirements.txt         # Python dependencies
├── setup_env.sh            # Environment setup script
├── start_app.sh            # Application startup script
├── README.md               # This file
├── static/                 # Web assets (CSS, JS)
│   ├── css/style.css
│   └── js/app.js
└── templates/              # HTML templates
    └── index.html
```

### 2. Environment Setup

#### Option A: Automatic Setup (Recommended)
Run the setup script to create and configure the conda environment:
```bash
chmod +x setup_env.sh
./setup_env.sh
```

#### Option B: Manual Setup
```bash
# Create conda environment
conda create -n ECG-Signal-Anomaly-Detection-Model python=3.9 -y

# Activate environment
conda activate ECG-Signal-Anomaly-Detection-Model

# Install dependencies
pip install -r requirements.txt
```

### 3. Verify Installation

Check that all required packages are installed:
```bash
conda activate ECG-Signal-Anomaly-Detection-Model
python -c "import flask, tensorflow, pandas, numpy, sklearn; print('✅ All packages imported successfully!')"
```

## 🚀 Running the Application

### Option A: Using the Startup Script (Recommended)
```bash
chmod +x start_app.sh
./start_app.sh
```

### Option B: Manual Start
```bash
# Activate the environment
conda activate ECG-Signal-Anomaly-Detection-Model

# Start the application
python app.py
```

### Option C: Alternative Manual Start
If you encounter issues with conda activation:
```bash
# Navigate to project directory
cd /path/to/ECG-Signal-Anomaly-Detection-Model

# Activate environment manually
source ~/anaconda3/etc/profile.d/conda.sh  # or ~/miniconda3/etc/profile.d/conda.sh
conda activate ECG-Signal-Anomaly-Detection-Model

# Run the app
python app.py
```

## 🌐 Accessing the Application

Once the application starts successfully, you'll see:
```
Loading data and model...
Loaded 100 rows of balanced ECG sample data
Label distribution:
  Label 0.0 (Normal): 50 samples
  Label 1.0 (Abnormal): 50 samples
Model loaded successfully
Starting Flask server...
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://[your-ip]:5001
```

**Access the application at: http://localhost:5001**

## 📊 Using the Application

### Main Interface
- **ECG Signal Plot**: Interactive visualization of ECG waveforms
- **Navigation Controls**: Browse through different ECG samples
- **Filter Options**: View all samples, normal only, or abnormal only
- **Prediction Results**: Real-time anomaly detection with confidence scores

### API Endpoints
- `GET /` - Main application interface
- `GET /api/data/<row_index>` - Get ECG data for specific row
- `GET /api/info` - Get dataset information
- `GET /api/filter/<filter_type>` - Get filtered sample indices
- `GET /api/data/filtered/<filter_type>/<filtered_index>` - Get filtered data

## 🔧 Project Structure

### Core Files
- **`app.py`**: Main Flask application with API endpoints
- **`ekg_model.keras`**: Pre-trained TensorFlow/Keras model for anomaly detection
- **`sample_mitbih.csv`**: Balanced dataset with 100 ECG samples (50 normal, 50 abnormal)
- **`ecg_sampler.py`**: Utilities for data sampling and preprocessing

### Web Interface
- **`templates/index.html`**: Main HTML template
- **`static/css/style.css`**: Styling for the web interface
- **`static/js/app.js`**: JavaScript for interactive functionality

### Configuration
- **`requirements.txt`**: Python package dependencies
- **`setup_env.sh`**: Automated environment setup script
- **`start_app.sh`**: Application startup script

## 🐛 Troubleshooting

### Common Issues

#### 1. Conda Environment Not Found
```bash
# List available environments
conda env list

# If environment doesn't exist, run setup
./setup_env.sh
```

#### 2. Module Import Errors
```bash
# Ensure environment is activated
conda activate ECG-Signal-Anomaly-Detection-Model

# Reinstall requirements
pip install -r requirements.txt
```

#### 3. Model Loading Error
- Ensure `ekg_model.keras` file exists in the project directory
- Check file permissions: `ls -la ekg_model.keras`
- Verify TensorFlow installation: `python -c "import tensorflow; print(tensorflow.__version__)"`

#### 4. Data Loading Error
- Ensure `sample_mitbih.csv` file exists
- Check file format and integrity
- Verify pandas installation: `python -c "import pandas; print(pandas.__version__)"`

#### 5. Port Already in Use
If port 5001 is occupied, modify `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5002)  # Change port number
```

#### 6. Conda Activation Issues
```bash
# Initialize conda for shell
conda init zsh  # or bash

# Restart terminal and try again
# Or use full path to conda
/opt/anaconda3/bin/conda activate ECG-Signal-Anomaly-Detection-Model
```

### Debug Mode
To run in debug mode for development:
```bash
export FLASK_DEBUG=1
python app.py
```

## 📝 Dependencies

### Core Requirements
- **Flask 2.0.1**: Web framework
- **TensorFlow 2.13.0**: Machine learning library
- **Pandas 2.0.3**: Data manipulation
- **NumPy 1.24.3**: Numerical computing
- **Scikit-learn 1.3.0**: Machine learning utilities

### Complete Dependency List
See `requirements.txt` for the full list of dependencies with exact versions.

## 🔬 Model Information

- **Model Type**: Neural Network (Keras/TensorFlow)
- **Input**: ECG signal data (normalized)
- **Output**: Binary classification (Normal/Abnormal)
- **Dataset**: MIT-BIH Arrhythmia Database sample
- **Performance**: Optimized for ECG anomaly detection

## 📈 Dataset Information

- **Source**: MIT-BIH Arrhythmia Database
- **Samples**: 100 balanced ECG signals
- **Distribution**: 50 normal, 50 abnormal cases
- **Format**: CSV with signal features and labels
- **Preprocessing**: MinMax scaling applied

## 🤝 Support

If you encounter issues:

1. **Check Prerequisites**: Ensure Anaconda/Miniconda is installed
2. **Environment Setup**: Verify the conda environment is properly configured
3. **File Integrity**: Ensure all required files are present
4. **Permissions**: Check file permissions for scripts and data files
5. **Port Conflicts**: Try different ports if 5001 is occupied

## 📄 License

This project is for educational and research purposes. Please ensure proper attribution when using the code or model.

---

**🎉 Happy ECG Analysis!**

For additional support or questions, please check the troubleshooting section or review the project structure for better understanding of the components.
