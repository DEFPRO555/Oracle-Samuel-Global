# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Enhanced Integration Script
# MD5-Protected AI System. Unauthorized use prohibited.

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

class OracleSamuelEnhancer:
    """
    Enhancement module for Oracle Samuel with K-means, confusion matrix, and logistic regression
    """
    
    def __init__(self, df, predictor=None):
        self.df = df.copy()
        self.predictor = predictor
        self.scaler = StandardScaler()
        self.kmeans_model = None
        self.logistic_model = None
        self.clusters = None
        self.price_categories = None
        self.confusion_matrix_data = None
        
    def enhance_with_kmeans(self, n_clusters=5):
        """Add K-means clustering for market segmentation"""
        st.info("🎯 Adding K-means clustering for market segmentation...")
        
        # Prepare numeric features for clustering
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        if 'price' in numeric_cols:
            numeric_cols.remove('price')
        
        if len(numeric_cols) < 2:
            return False, "Insufficient numeric features for clustering"
        
        X_cluster = self.df[numeric_cols].fillna(0)
        X_scaled = self.scaler.fit_transform(X_cluster)
        
        # Determine optimal number of clusters
        inertias = []
        silhouette_scores = []
        K_range = range(2, min(8, len(X_scaled)//10))
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X_scaled)
            inertias.append(kmeans.inertia_)
            
            from sklearn.metrics import silhouette_score
            silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
        
        # Find optimal k
        optimal_k = K_range[np.argmax(silhouette_scores)]
        
        # Perform final clustering
        self.kmeans_model = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
        self.clusters = self.kmeans_model.fit_predict(X_scaled)
        
        # Add cluster information to dataframe
        self.df['market_cluster'] = self.clusters
        
        # Analyze clusters
        cluster_analysis = self._analyze_clusters()
        
        return True, {
            'optimal_clusters': optimal_k,
            'silhouette_score': max(silhouette_scores),
            'cluster_analysis': cluster_analysis
        }
    
    def _analyze_clusters(self):
        """Analyze cluster characteristics"""
        analysis = {}
        
        for cluster_id in np.unique(self.clusters):
            cluster_data = self.df[self.df['market_cluster'] == cluster_id]
            
            # Find price column
            price_col = None
            for col in self.df.columns:
                if 'price' in col.lower():
                    price_col = col
                    break
            
            if price_col:
                analysis[cluster_id] = {
                    'size': len(cluster_data),
                    'avg_price': cluster_data[price_col].mean(),
                    'price_std': cluster_data[price_col].std(),
                    'price_range': f"${cluster_data[price_col].min():,.0f} - ${cluster_data[price_col].max():,.0f}"
                }
        
        return analysis
    
    def enhance_with_logistic_regression(self):
        """Add logistic regression for price category classification"""
        st.info("📊 Adding logistic regression for price category classification...")
        
        # Find price column
        price_col = None
        for col in self.df.columns:
            if 'price' in col.lower():
                price_col = col
                break
        
        if not price_col:
            return False, "No price column found"
        
        # Create price categories
        price_quartiles = np.percentile(self.df[price_col], [25, 50, 75])
        
        def categorize_price(price):
            if price <= price_quartiles[0]:
                return 'Low'
            elif price <= price_quartiles[1]:
                return 'Medium-Low'
            elif price <= price_quartiles[2]:
                return 'Medium-High'
            else:
                return 'High'
        
        self.price_categories = self.df[price_col].apply(categorize_price)
        self.df['price_category'] = self.price_categories
        
        # Prepare features for logistic regression
        feature_cols = [col for col in self.df.columns if col not in [price_col, 'price_category', 'market_cluster']]
        X = self.df[feature_cols].select_dtypes(include=[np.number]).fillna(0)
        
        if len(X.columns) == 0:
            return False, "No suitable features for logistic regression"
        
        # Train logistic regression
        from sklearn.model_selection import train_test_split
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, self.price_categories, test_size=0.2, random_state=42, stratify=self.price_categories
        )
        
        self.logistic_model = LogisticRegression(random_state=42, max_iter=1000)
        self.logistic_model.fit(X_train, y_train)
        
        # Generate confusion matrix
        y_pred = self.logistic_model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.confusion_matrix_data = {
            'matrix': cm,
            'accuracy': accuracy,
            'classes': self.logistic_model.classes_,
            'classification_report': classification_report(y_test, y_pred)
        }
        
        return True, {
            'accuracy': accuracy,
            'confusion_matrix': cm,
            'classes': self.logistic_model.classes_
        }
    
    def create_enhanced_visualizations(self):
        """Create enhanced visualizations with clustering and confusion matrix"""
        visualizations = {}
        
        # 1. Cluster Analysis Visualization
        if self.clusters is not None:
            price_col = None
            for col in self.df.columns:
                if 'price' in col.lower():
                    price_col = col
                    break
            
            if price_col:
                fig_cluster = px.scatter(
                    self.df, 
                    x='market_cluster', 
                    y=price_col,
                    color='market_cluster',
                    title='Market Clusters by Price',
                    labels={'market_cluster': 'Market Cluster', price_col: 'Price ($)'}
                )
                visualizations['cluster_analysis'] = fig_cluster
        
        # 2. Confusion Matrix Heatmap
        if self.confusion_matrix_data is not None:
            cm = self.confusion_matrix_data['matrix']
            classes = self.confusion_matrix_data['classes']
            
            fig_cm = px.imshow(
                cm,
                text_auto=True,
                aspect="auto",
                title=f'Confusion Matrix (Accuracy: {self.confusion_matrix_data["accuracy"]:.3f})',
                labels=dict(x="Predicted", y="Actual", color="Count")
            )
            fig_cm.update_xaxes(tickmode='array', tickvals=list(range(len(classes))), ticktext=classes)
            fig_cm.update_yaxes(tickmode='array', tickvals=list(range(len(classes))), ticktext=classes)
            visualizations['confusion_matrix'] = fig_cm
        
        # 3. Price Category Distribution
        if self.price_categories is not None:
            category_counts = self.price_categories.value_counts()
            fig_categories = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title='Price Category Distribution'
            )
            visualizations['price_categories'] = fig_categories
        
        return visualizations
    
    def generate_enhancement_report(self):
        """Generate comprehensive enhancement report"""
        report = "🚀 ORACLE SAMUEL ENHANCEMENT REPORT\n"
        report += "=" * 50 + "\n\n"
        
        # K-means clustering report
        if self.clusters is not None:
            report += "🎯 K-MEANS CLUSTERING ANALYSIS\n"
            report += "-" * 30 + "\n"
            report += f"Number of clusters: {len(np.unique(self.clusters))}\n"
            
            cluster_analysis = self._analyze_clusters()
            for cluster_id, data in cluster_analysis.items():
                report += f"\nCluster {cluster_id}:\n"
                report += f"  Size: {data['size']} properties\n"
                report += f"  Average Price: ${data['avg_price']:,.0f}\n"
                report += f"  Price Range: {data['price_range']}\n"
            
            report += "\n"
        
        # Logistic regression report
        if self.confusion_matrix_data is not None:
            report += "📊 LOGISTIC REGRESSION ANALYSIS\n"
            report += "-" * 30 + "\n"
            report += f"Classification Accuracy: {self.confusion_matrix_data['accuracy']:.3f}\n"
            report += f"Price Categories: {', '.join(self.confusion_matrix_data['classes'])}\n"
            report += f"\nClassification Report:\n{self.confusion_matrix_data['classification_report']}\n"
        
        return report
    
    def predict_enhanced(self, input_data):
        """Enhanced prediction with clustering and category information"""
        if self.predictor is None:
            return None, "No base predictor available"
        
        try:
            # Get base prediction
            base_prediction, error = self.predictor.predict_price(input_data)
            if error:
                return None, error
            
            # Get cluster assignment if available
            cluster_info = None
            if self.kmeans_model is not None:
                # Prepare input for clustering
                numeric_cols = [col for col in input_data.keys() if isinstance(input_data[col], (int, float))]
                if len(numeric_cols) >= 2:
                    cluster_input = np.array([[input_data[col] for col in numeric_cols]])
                    cluster_input_scaled = self.scaler.transform(cluster_input)
                    cluster = self.kmeans_model.predict(cluster_input_scaled)[0]
                    cluster_info = f"Market Cluster {cluster}"
            
            # Get price category if available
            category_info = None
            if self.logistic_model is not None and base_prediction:
                # Create price category based on prediction
                price_quartiles = np.percentile(self.df[[col for col in self.df.columns if 'price' in col.lower()][0]], [25, 50, 75])
                
                if base_prediction <= price_quartiles[0]:
                    category = 'Low'
                elif base_prediction <= price_quartiles[1]:
                    category = 'Medium-Low'
                elif base_prediction <= price_quartiles[2]:
                    category = 'Medium-High'
                else:
                    category = 'High'
                
                category_info = f"Price Category: {category}"
            
            # Enhanced result
            enhanced_result = {
                'predicted_price': base_prediction,
                'cluster_info': cluster_info,
                'category_info': category_info,
                'enhancement_features': {
                    'kmeans_clustering': self.kmeans_model is not None,
                    'logistic_regression': self.logistic_model is not None,
                    'confusion_matrix': self.confusion_matrix_data is not None
                }
            }
            
            return enhanced_result, None
            
        except Exception as e:
            return None, f"Enhanced prediction error: {str(e)}"

def integrate_enhancements_to_app():
    """Integration function to add enhancements to the main app"""
    
    # Add to the main app.py file
    integration_code = '''
# Add this to your app.py imports
from oracle_samuel_enhancement import OracleSamuelEnhancer

# Add this to your session state initialization
if 'enhancer' not in st.session_state:
    st.session_state.enhancer = None

# Add this to your data processing section (after data is cleaned)
if st.session_state.cleaned_df is not None:
    # Initialize enhancer
    st.session_state.enhancer = OracleSamuelEnhancer(
        st.session_state.cleaned_df, 
        st.session_state.predictor
    )
    
    # Add enhancement buttons to your UI
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Add K-means Clustering"):
            success, result = st.session_state.enhancer.enhance_with_kmeans()
            if success:
                st.success(f"✅ K-means clustering added! {result['optimal_clusters']} clusters found")
            else:
                st.error(f"❌ {result}")
    
    with col2:
        if st.button("📊 Add Logistic Regression"):
            success, result = st.session_state.enhancer.enhance_with_logistic_regression()
            if success:
                st.success(f"✅ Logistic regression added! Accuracy: {result['accuracy']:.3f}")
            else:
                st.error(f"❌ {result}")
    
    with col3:
        if st.button("📈 Generate Enhanced Report"):
            report = st.session_state.enhancer.generate_enhancement_report()
            st.text(report)
    
    # Add enhanced visualizations
    if st.session_state.enhancer:
        visualizations = st.session_state.enhancer.create_enhanced_visualizations()
        
        for viz_name, fig in visualizations.items():
            st.plotly_chart(fig, use_container_width=True)
    '''
    
    return integration_code

# Example usage function
def demonstrate_enhancements():
    """Demonstrate the enhancement features"""
    st.title("🚀 Oracle Samuel Enhancements Demo")
    
    # Create sample data
    np.random.seed(42)
    n_samples = 500
    
    sample_data = {
        'bedrooms': np.random.randint(1, 6, n_samples),
        'bathrooms': np.random.randint(1, 4, n_samples),
        'sqft_living': np.random.randint(800, 4000, n_samples),
        'price': np.random.randint(200000, 1500000, n_samples)
    }
    
    df = pd.DataFrame(sample_data)
    
    # Initialize enhancer
    enhancer = OracleSamuelEnhancer(df)
    
    # Demonstrate K-means clustering
    st.subheader("🎯 K-means Clustering Enhancement")
    success, result = enhancer.enhance_with_kmeans()
    if success:
        st.success(f"✅ K-means clustering completed!")
        st.write(f"Optimal clusters: {result['optimal_clusters']}")
        st.write(f"Silhouette score: {result['silhouette_score']:.3f}")
    
    # Demonstrate logistic regression
    st.subheader("📊 Logistic Regression Enhancement")
    success, result = enhancer.enhance_with_logistic_regression()
    if success:
        st.success(f"✅ Logistic regression completed!")
        st.write(f"Classification accuracy: {result['accuracy']:.3f}")
    
    # Show visualizations
    st.subheader("📈 Enhanced Visualizations")
    visualizations = enhancer.create_enhanced_visualizations()
    
    for viz_name, fig in visualizations.items():
        st.plotly_chart(fig, use_container_width=True)
    
    # Show enhancement report
    st.subheader("📋 Enhancement Report")
    report = enhancer.generate_enhancement_report()
    st.text(report)

if __name__ == "__main__":
    # Run demonstration
    demonstrate_enhancements()
