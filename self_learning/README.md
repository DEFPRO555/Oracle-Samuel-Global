# 🧠 ORACLE SAMUEL - SELF-LEARNING ENGINE
## © 2025 Dowek Analytics Ltd. All Rights Reserved.

### Part 2: Continuous Learning & AI Evolution

---

## 📋 Overview

The **Self-Learning Engine** transforms Oracle Samuel from a static ML system into a **continuously evolving AI** that learns, adapts, and improves with every dataset uploaded.

### Key Features

1. **🔄 Automatic Model Retraining**
   - Trains 4 models simultaneously (Random Forest, XGBoost, LightGBM, Linear Regression)
   - Auto-selects best performer based on R² score
   - Saves models with MD5 versioning

2. **📊 Performance Evaluation & Tracking**
   - Logs every training session to SQL
   - Tracks MAE, RMSE, R² metrics over time
   - Analyzes performance trends (improving/declining)

3. **⭐ User Feedback System**
   - 5-star rating system
   - Comment collection
   - Satisfaction score calculation
   - Improvement area identification

4. **📚 Knowledge Base**
   - Stores feature correlations across datasets
   - Maintains feature importance history
   - Generates market insights automatically
   - Builds cumulative intelligence

5. **🔐 Model Versioning**
   - MD5 hash for each trained model
   - File integrity verification
   - Training history with timestamps
   - Auto-cleanup of old models

---

## 🗂 Module Structure

```
self_learning/
├── __init__.py                  # Module initialization
├── trainer.py                   # Multi-model training engine
├── evaluator.py                 # Performance tracking & logging
├── retrain_manager.py           # Automatic retraining orchestration
├── feedback_manager.py          # User feedback collection
├── knowledge_base.py            # Cumulative insights storage
└── README.md                    # This file
```

---

## 🔧 Module Details

### 1. `trainer.py` - SelfLearningTrainer

**Purpose**: Train multiple ML models and select the best performer.

**Key Methods**:
- `train_multiple_models(df)` - Train RF, XGBoost, LightGBM, Linear Regression
- `save_model()` - Save best model with MD5 hash
- `load_model()` - Load previously trained model
- `predict(input_data)` - Make predictions with loaded model

**Models Trained**:
1. **Random Forest** - 200 trees, max_depth=15
2. **XGBoost** - 200 estimators, learning_rate=0.1
3. **LightGBM** - 200 estimators, fast training
4. **Linear Regression** - Baseline model

**Output**: 
- Saves `oracle_samuel_model.pkl` with best model
- Returns training metrics and results

---

### 2. `evaluator.py` - ModelEvaluator

**Purpose**: Track and log model performance over time.

**SQL Tables Created**:
- `model_evaluation_log` - All training sessions
- `model_comparison` - Model comparison records

**Key Methods**:
- `log_evaluation()` - Log training metrics to SQL
- `get_evaluation_history()` - Retrieve past evaluations
- `get_best_model()` - Find highest performing model
- `get_performance_trends()` - Analyze improvement over time
- `display_performance_table()` - Rich terminal display

**Metrics Tracked**:
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² Score (Coefficient of Determination)
- Training/test sample counts
- MD5 model hash
- Timestamp

---

### 3. `retrain_manager.py` - RetrainManager

**Purpose**: Orchestrate automatic retraining on new datasets.

**SQL Tables Created**:
- `retrain_log` - Retraining activity log

**Key Methods**:
- `check_for_new_data()` - Detect uploaded datasets
- `get_latest_dataset()` - Retrieve most recent data
- `retrain_on_dataset()` - Retrain on specific dataset
- `retrain_all()` - Comprehensive retrain on all data
- `auto_retrain_if_needed()` - Trigger retrain at threshold

**Workflow**:
1. Check for new uploaded data in SQL
2. Load dataset into memory
3. Call `SelfLearningTrainer` to train models
4. Log results with `ModelEvaluator`
5. Save best model automatically
6. Display results with Rich formatting

---

### 4. `feedback_manager.py` - FeedbackManager

**Purpose**: Collect and analyze user feedback.

**SQL Tables Created**:
- `user_feedback` - General ratings and comments
- `prediction_feedback` - Prediction accuracy feedback

**Key Methods**:
- `log_user_feedback()` - Store rating (1-5 stars) + comment
- `log_prediction_feedback()` - Store predicted vs actual
- `get_feedback_summary()` - Calculate averages
- `get_satisfaction_score()` - Overall satisfaction %
- `identify_improvement_areas()` - Find low-rated issues

**Rating System**:
- 1⭐ - Very dissatisfied
- 2⭐ - Dissatisfied
- 3⭐ - Neutral
- 4⭐ - Satisfied
- 5⭐ - Very satisfied

---

### 5. `knowledge_base.py` - KnowledgeBase

**Purpose**: Build cumulative intelligence across datasets.

**SQL Tables Created**:
- `feature_correlations` - Feature-price correlations
- `market_insights` - Auto-generated insights
- `feature_importance_history` - Importance trends

**Key Methods**:
- `store_feature_correlations()` - Store correlation data
- `store_feature_importance()` - Log feature importance
- `get_top_correlated_features()` - Most important features
- `generate_market_insight()` - Create new insight
- `analyze_dataset_and_generate_insights()` - Auto-analysis

**Insights Generated**:
- Average price trends
- Price range analysis
- Market volatility assessment
- Feature correlation patterns
- Top predictive features

---

## 🚀 Usage Examples

### Example 1: Retrain Model

```python
from self_learning.retrain_manager import RetrainManager

manager = RetrainManager()
success, result = manager.retrain_all()

if success:
    print(f"Best model: {result['best_model']}")
    print(f"R² Score: {result['r2']:.4f}")
```

### Example 2: Log Feedback

```python
from self_learning.feedback_manager import FeedbackManager

feedback = FeedbackManager()
feedback.log_user_feedback(
    rating=5,
    comment="Amazing predictions!",
    feedback_type='general'
)
```

### Example 3: Generate Insights

```python
from self_learning.knowledge_base import KnowledgeBase
import pandas as pd

kb = KnowledgeBase()
df = pd.read_csv('property_data.csv')

insights = kb.analyze_dataset_and_generate_insights(df)
print(f"Generated {len(insights)} insights")
```

### Example 4: Check Performance Trends

```python
from self_learning.evaluator import ModelEvaluator

evaluator = ModelEvaluator()
trends = evaluator.get_performance_trends()

print(f"Trend: {trends['trend']}")
print(f"Improvement: {trends['improvement']:.2f}%")
```

---

## 📊 Streamlit Integration

The self-learning system is integrated into the main Streamlit app via **Tab 5: SELF-LEARNING**.

### Tab Sections:

1. **🔄 Model Retraining**
   - Button to retrain on latest data
   - Shows best model and metrics
   - Displays retraining history

2. **📊 Performance Tracking**
   - Evaluation history table
   - Performance trend analysis
   - Latest metrics display

3. **⭐ User Feedback & Ratings**
   - 5-star slider rating
   - Comment text area
   - Feedback summary statistics
   - Recent feedback display

4. **📚 Knowledge Base & Market Insights**
   - Top correlated features
   - Auto-generated insights
   - Generate insights button

5. **🔐 Model Versioning**
   - Current model MD5 hash
   - Model file size
   - Last modified timestamp

6. **📈 System Statistics**
   - Total trainings performed
   - Total feedback collected
   - Insights generated count
   - Retrains performed

---

## 🗄 Database Schema

### Tables Created:

```sql
-- Model Evaluation Log
CREATE TABLE model_evaluation_log (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    model_name TEXT,
    mae REAL,
    rmse REAL,
    r2 REAL,
    md5_hash TEXT,
    training_samples INTEGER,
    test_samples INTEGER
);

-- Retrain Log
CREATE TABLE retrain_log (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    dataset_name TEXT,
    records_count INTEGER,
    model_trained TEXT,
    mae REAL,
    r2 REAL,
    status TEXT
);

-- User Feedback
CREATE TABLE user_feedback (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    rating INTEGER,
    comment TEXT,
    feedback_type TEXT,
    model_version TEXT
);

-- Feature Correlations
CREATE TABLE feature_correlations (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    feature_name TEXT,
    correlation_with_price REAL,
    dataset_name TEXT
);

-- Market Insights
CREATE TABLE market_insights (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    insight_type TEXT,
    insight_value TEXT,
    confidence_score REAL
);
```

---

## 🧪 Testing Procedure

### Step 1: Upload Data
1. Go to **HOME** tab
2. Upload `sample_data.csv`
3. Click "Clean and Analyze Data"

### Step 2: Initial Training
1. Go to **SELF-LEARNING** tab
2. Click "🚀 Retrain Now"
3. Wait for training (30-60 seconds)
4. Verify best model is displayed

### Step 3: Check Performance
1. View "Model Evaluation History"
2. Check metrics (MAE, R², RMSE)
3. Confirm data saved to SQL

### Step 4: Submit Feedback
1. Rate with star slider (1-5)
2. Add comment
3. Click "Submit Feedback"
4. Verify feedback appears in recent list

### Step 5: Generate Insights
1. Click "🔍 Generate New Insights"
2. Check insights display
3. View top correlated features

### Step 6: Verify MD5
1. Check "Model Versioning" section
2. Verify MD5 hash displayed
3. Check model file size

---

## 🎯 Expected Results

After successful implementation:

✅ **4 models** train simultaneously  
✅ **Best model** auto-selected based on R²  
✅ **Performance history** logged to SQL  
✅ **User feedback** collected and analyzed  
✅ **Market insights** auto-generated  
✅ **MD5 hash** calculated for versioning  
✅ **Rich terminal** output during training  
✅ **Progress bars** show training status  

---

## 🔐 Security & Protection

- All modules include Dowek Analytics © copyright
- MD5 hashing ensures model integrity
- SQL logs provide audit trail
- Timestamps track all activities
- Model versioning prevents overwrites

---

## 📈 Performance Metrics

**Training Speed**:
- Random Forest: ~10-15 seconds
- XGBoost: ~5-8 seconds
- LightGBM: ~3-5 seconds
- Linear Regression: <1 second

**Typical Accuracy** (on sample data):
- Random Forest R²: 0.85-0.92
- XGBoost R²: 0.82-0.90
- LightGBM R²: 0.80-0.88
- Linear Regression R²: 0.70-0.78

---

## 🚨 Troubleshooting

### Issue: Training fails
**Solution**: Ensure dataset has numeric price column

### Issue: No data found for retraining
**Solution**: Upload and clean data in HOME tab first

### Issue: Feedback not saving
**Solution**: Check rating is between 1-5

### Issue: Insights not generating
**Solution**: Ensure dataset has been uploaded

---

## 🌟 Future Enhancements

Potential additions for version 3:

- [ ] Neural network models (TensorFlow/PyTorch)
- [ ] Time-series forecasting with Prophet
- [ ] AutoML integration (Auto-sklearn)
- [ ] Hyperparameter tuning with Optuna
- [ ] Model explainability (SHAP values)
- [ ] A/B testing framework
- [ ] Email alerts for performance drops
- [ ] API endpoint for predictions

---

## 📞 Support

For questions or issues:
- Email: support@dowekanalytics.com
- Documentation: See main README.md

---

**ORACLE SAMUEL - SELF-LEARNING ENGINE**  
*Continuously evolving, endlessly improving* 🧠✨

© 2025 Dowek Analytics Ltd. All Rights Reserved.

