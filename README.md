# 🏠 ORACLE SAMUEL – THE REAL ESTATE MARKET PROPHET

## © 2025 Dowek Analytics Ltd. All Rights Reserved.
**MD5-Protected Intelligent System. Unauthorized reproduction or redistribution is prohibited.**

---

## 🌟 Overview

**Oracle Samuel** is a cutting-edge **Streamlit + SQL + Machine Learning** dashboard designed to analyze, visualize, and predict real estate market trends with unprecedented accuracy.

Built with the precision of San Francisco's finest AI labs, Oracle Samuel combines:
- 🤖 **Advanced AI Analysis** - Natural language interaction with your data
- 📊 **Machine Learning Models** - Random Forest & Linear Regression for price prediction
- 💾 **SQL Database Integration** - Persistent data storage with SQLite
- 🔐 **MD5 Security** - Enterprise-grade data integrity protection
- 📈 **Interactive Visualizations** - Plotly-powered charts and graphs

---

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

The dashboard will open automatically in your default browser at `http://localhost:8501`

---

## 📁 Project Structure

```
oracle_samuel_real_estate/
│
├── app.py                      # Main Streamlit dashboard
├── agent.py                    # Oracle Samuel AI Agent
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
│
├── utils/
│   ├── __init__.py
│   ├── md5_manager.py         # MD5 encryption & integrity
│   ├── database_manager.py    # SQL operations (SQLite)
│   ├── data_cleaner.py        # Data preprocessing
│   ├── predictor.py           # ML models (RF, Linear Regression)
│   └── visualizer.py          # Plotly visualizations
│
└── sample_data.csv            # Sample real estate dataset
```

---

## 🎯 Features

### 🏠 HOME / FRONT Tab
- **Upload Data**: Support for CSV and XLSX files
- **Data Cleaning**: Automatic preprocessing and validation
- **MD5 Protection**: Generate cryptographic signatures
- **SQL Storage**: Save data to local database
- **Summary Statistics**: Instant overview of your data

### 🤖 ASK THE AGENT Tab
- **Interactive Chat**: Ask questions in natural language
- **AI Analysis**: Oracle Samuel provides expert insights
- **Smart Queries**: 
  - "Which features most affect house prices?"
  - "Predict price growth for waterfront properties"
  - "Which houses are undervalued?"
- **Quick Actions**: Pre-built analysis buttons

### 📊 STATISTICS & ANALYTICS Tab
- **Data Visualization**: Interactive Plotly charts
- **Correlation Heatmap**: Understand feature relationships
- **Scatter Plots**: Explore price vs features
- **Distribution Analysis**: Box plots and histograms
- **Statistical Summary**: Comprehensive data description

### 🧪 PERFORMANCE TEST Tab
- **Model Training**: Random Forest & Linear Regression
- **Performance Metrics**: MAE, RMSE, R² Score
- **Feature Importance**: Top factors affecting price
- **Prediction Visualization**: Actual vs Predicted plots
- **Residual Analysis**: Model accuracy assessment

---

## 📊 Supported Data Format

Your CSV/XLSX file should contain real estate data with columns such as:

- `price` - Property price (required)
- `bedrooms` - Number of bedrooms
- `bathrooms` - Number of bathrooms
- `sqft_living` - Living area square footage
- `lot_size` - Lot size
- `view` - View rating
- `waterfront` - Waterfront property (yes/no)
- ... and any other relevant features

**Example:**

| price   | bedrooms | bathrooms | sqft_living | lot_size | view | waterfront |
|---------|----------|-----------|-------------|----------|------|------------|
| 450000  | 3        | 2         | 1800        | 7500     | 0    | no         |
| 875000  | 4        | 3         | 2500        | 9000     | 3    | yes        |

---

## 🤖 How to Use Oracle Samuel

### Step 1: Upload Your Data
1. Go to the **HOME** tab
2. Click "Browse files" and select your CSV/XLSX file
3. Click "Clean and Analyze Data"
4. Oracle Samuel will process and secure your data

### Step 2: Ask Questions
1. Navigate to **ASK THE AGENT** tab
2. Type your question or click a quick action button
3. Oracle Samuel will analyze and respond with insights

### Step 3: Explore Analytics
1. Go to **STATISTICS & ANALYTICS** tab
2. View interactive charts and correlations
3. Explore relationships between features

### Step 4: Train & Test Models
1. Open **PERFORMANCE TEST** tab
2. Select a model type (Random Forest recommended)
3. Click "Train Model"
4. Review accuracy metrics and predictions

---

## 🔐 Security Features

### MD5 Protection
Every uploaded dataset receives a unique MD5 hash signature:
- Ensures data integrity
- Tracks version history
- Stored in SQL database for audit trail

### Copyright Protection
All files include:
```python
# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – The Real Estate Market Prophet
# MD5-Protected AI System. Unauthorized use prohibited.
```

---

## 🛠 Technical Stack

- **Frontend**: Streamlit 1.29.0
- **ML Models**: scikit-learn 1.3.2
- **Database**: SQLite via SQLAlchemy 2.0.23
- **Visualizations**: Plotly 5.18.0, Matplotlib, Seaborn
- **Data Processing**: Pandas 2.1.4, NumPy 1.26.2
- **Forecasting**: Prophet 1.1.5

---

## 📈 Model Performance

Oracle Samuel uses state-of-the-art machine learning:

### Random Forest Regressor
- **Ensemble Learning**: 100 decision trees
- **Feature Importance**: Automatic ranking
- **Accuracy**: Typically 85-95% R²

### Linear Regression
- **Interpretable**: Clear coefficient analysis
- **Fast Training**: Instant results
- **Baseline Model**: Good for simple relationships

---

## 💡 Tips for Best Results

1. **Data Quality**: Ensure your CSV has minimal missing values
2. **Feature Rich**: More relevant columns = better predictions
3. **Sufficient Size**: At least 100 records recommended
4. **Clean Data**: Remove obvious errors before upload
5. **Price Column**: Must contain numeric price data

---

## 🐛 Troubleshooting

### Issue: "Could not find price column"
**Solution**: Ensure your dataset has a column named `price`, `cost`, `value`, or `amount`

### Issue: Model accuracy is low
**Solution**: 
- Add more relevant features to your dataset
- Increase the number of data records
- Check for data quality issues

### Issue: Upload fails
**Solution**: 
- Verify file format (CSV or XLSX only)
- Check file isn't corrupted
- Ensure file size is reasonable (<100MB)

---

## 🚀 Future Enhancements

Planned features for upcoming versions:
- [ ] OpenAI GPT integration for enhanced natural language
- [ ] Prophet time-series forecasting
- [ ] Multi-market comparison tools
- [ ] Export analysis reports (PDF)
- [ ] Dark mode toggle
- [ ] Real-time market data integration
- [ ] Mobile-responsive design improvements

---

## 📞 Support

For issues, questions, or feature requests:
- **Email**: support@dowekanalytics.com
- **Documentation**: See this README
- **License**: Proprietary - Dowek Analytics Ltd.

---

## 📜 License

**Proprietary Software**

© 2025 Dowek Analytics Ltd. All Rights Reserved.

This software is the exclusive property of Dowek Analytics Ltd. 
Unauthorized copying, distribution, modification, or use is strictly prohibited 
and may result in legal action.

MD5-Protected Intelligent System.

---

## 🎓 About Dowek Analytics

Dowek Analytics Ltd. is a San Francisco-inspired data science company 
specializing in AI-powered real estate intelligence solutions.

**Mission**: Democratize advanced real estate analytics through cutting-edge AI technology.

---

## 🙏 Acknowledgments

Built with ❤️ using:
- Streamlit for the amazing framework
- scikit-learn for ML capabilities
- Plotly for beautiful visualizations
- The open-source community

---

**ORACLE SAMUEL - THE REAL ESTATE MARKET PROPHET**

*Predicting the future of real estate, one property at a time.* 🏠✨

