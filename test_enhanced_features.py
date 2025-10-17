# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Enhanced Features Test Script
# MD5-Protected AI System. Unauthorized use prohibited.

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

def create_sample_data():
    """Create sample real estate data for testing"""
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'bedrooms': np.random.randint(1, 6, n_samples),
        'bathrooms': np.random.randint(1, 4, n_samples),
        'sqft_living': np.random.randint(800, 4000, n_samples),
        'sqft_lot': np.random.randint(2000, 20000, n_samples),
        'floors': np.random.choice([1, 1.5, 2, 2.5, 3], n_samples),
        'waterfront': np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
        'view': np.random.randint(0, 5, n_samples),
        'condition': np.random.randint(1, 6, n_samples),
        'grade': np.random.randint(6, 14, n_samples),
        'yr_built': np.random.randint(1900, 2020, n_samples),
        'price': np.random.randint(200000, 2000000, n_samples)
    }
    
    return pd.DataFrame(data)

def test_kmeans_clustering(df):
    """Test K-means clustering functionality"""
    print("🎯 Testing K-means Clustering...")
    
    # Prepare features
    numeric_cols = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'view', 'condition', 'grade']
    X = df[numeric_cols]
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Determine optimal clusters
    inertias = []
    silhouette_scores = []
    K_range = range(2, 8)
    
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        
        from sklearn.metrics import silhouette_score
        silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
    
    optimal_k = K_range[np.argmax(silhouette_scores)]
    print(f"✓ Optimal clusters: {optimal_k}")
    print(f"✓ Best silhouette score: {max(silhouette_scores):.3f}")
    
    # Perform final clustering
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    
    # Analyze clusters
    df['cluster'] = clusters
    cluster_analysis = {}
    
    for cluster_id in np.unique(clusters):
        cluster_data = df[df['cluster'] == cluster_id]
        cluster_analysis[cluster_id] = {
            'size': len(cluster_data),
            'avg_price': cluster_data['price'].mean(),
            'price_std': cluster_data['price'].std(),
            'avg_bedrooms': cluster_data['bedrooms'].mean(),
            'avg_sqft': cluster_data['sqft_living'].mean()
        }
    
    print("\n📊 Cluster Analysis:")
    for cluster_id, data in cluster_analysis.items():
        print(f"Cluster {cluster_id}: {data['size']} properties, "
              f"Avg Price: ${data['avg_price']:,.0f}, "
              f"Avg Bedrooms: {data['avg_bedrooms']:.1f}")
    
    return kmeans, clusters, cluster_analysis

def test_logistic_regression(df):
    """Test logistic regression for price categorization"""
    print("\n📊 Testing Logistic Regression...")
    
    # Create price categories
    price_quartiles = np.percentile(df['price'], [25, 50, 75])
    
    def categorize_price(price):
        if price <= price_quartiles[0]:
            return 'Low'
        elif price <= price_quartiles[1]:
            return 'Medium-Low'
        elif price <= price_quartiles[2]:
            return 'Medium-High'
        else:
            return 'High'
    
    df['price_category'] = df['price'].apply(categorize_price)
    
    # Prepare features
    feature_cols = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'view', 'condition', 'grade']
    X = df[feature_cols]
    y = df['price_category']
    
    # Split data
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train logistic regression
    log_reg = LogisticRegression(random_state=42, max_iter=1000)
    log_reg.fit(X_train, y_train)
    
    # Make predictions
    y_pred = log_reg.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    print(f"✓ Classification accuracy: {accuracy:.3f}")
    print(f"✓ Price categories: {', '.join(log_reg.classes_)}")
    
    print("\n📊 Confusion Matrix:")
    print(cm)
    
    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    return log_reg, cm, accuracy

def test_enhanced_prediction(df, kmeans_model, log_reg_model):
    """Test enhanced prediction with clustering and categorization"""
    print("\n🎯 Testing Enhanced Prediction...")
    
    # Sample input
    test_input = {
        'bedrooms': 3,
        'bathrooms': 2,
        'sqft_living': 2000,
        'sqft_lot': 8000,
        'floors': 2,
        'view': 2,
        'condition': 4,
        'grade': 8
    }
    
    # Prepare input for clustering
    numeric_cols = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'view', 'condition', 'grade']
    cluster_input = np.array([[test_input[col] for col in numeric_cols]])
    
    # Scale input
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[numeric_cols])
    cluster_input_scaled = scaler.transform(cluster_input)
    
    # Get cluster assignment
    cluster = kmeans_model.predict(cluster_input_scaled)[0]
    
    # Get price category prediction
    category = log_reg_model.predict(cluster_input)[0]
    
    # Simulate price prediction (in real app, this would come from your predictor)
    estimated_price = 500000  # This would be from your actual model
    
    print(f"✓ Test Property Features:")
    for key, value in test_input.items():
        print(f"  {key}: {value}")
    
    print(f"\n✓ Enhanced Prediction Results:")
    print(f"  Estimated Price: ${estimated_price:,.0f}")
    print(f"  Market Cluster: {cluster}")
    print(f"  Price Category: {category}")
    
    return {
        'estimated_price': estimated_price,
        'cluster': cluster,
        'category': category
    }

def create_visualizations(df):
    """Create visualizations for the enhanced features"""
    print("\n📈 Creating Visualizations...")
    
    # Set up the plotting style
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Oracle Samuel Enhanced Features Analysis', fontsize=16, fontweight='bold')
    
    # 1. Cluster Analysis
    if 'cluster' in df.columns:
        cluster_prices = df.groupby('cluster')['price'].mean()
        axes[0, 0].bar(cluster_prices.index, cluster_prices.values, color='skyblue', alpha=0.7)
        axes[0, 0].set_title('Average Price by Cluster')
        axes[0, 0].set_xlabel('Cluster')
        axes[0, 0].set_ylabel('Average Price ($)')
        axes[0, 0].ticklabel_format(style='plain', axis='y')
    
    # 2. Price Category Distribution
    if 'price_category' in df.columns:
        category_counts = df['price_category'].value_counts()
        axes[0, 1].pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%')
        axes[0, 1].set_title('Price Category Distribution')
    
    # 3. Price vs Square Footage by Cluster
    if 'cluster' in df.columns:
        for cluster_id in df['cluster'].unique():
            cluster_data = df[df['cluster'] == cluster_id]
            axes[1, 0].scatter(cluster_data['sqft_living'], cluster_data['price'], 
                             label=f'Cluster {cluster_id}', alpha=0.6)
        axes[1, 0].set_title('Price vs Square Footage by Cluster')
        axes[1, 0].set_xlabel('Square Footage')
        axes[1, 0].set_ylabel('Price ($)')
        axes[1, 0].legend()
        axes[1, 0].ticklabel_format(style='plain', axis='y')
    
    # 4. Bedrooms vs Price by Category
    if 'price_category' in df.columns:
        for category in df['price_category'].unique():
            category_data = df[df['price_category'] == category]
            axes[1, 1].scatter(category_data['bedrooms'], category_data['price'], 
                             label=category, alpha=0.6)
        axes[1, 1].set_title('Bedrooms vs Price by Category')
        axes[1, 1].set_xlabel('Bedrooms')
        axes[1, 1].set_ylabel('Price ($)')
        axes[1, 1].legend()
        axes[1, 1].ticklabel_format(style='plain', axis='y')
    
    plt.tight_layout()
    plt.savefig('oracle_samuel_enhanced_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Visualizations saved as 'oracle_samuel_enhanced_analysis.png'")
    
    return fig

def main():
    """Main test function"""
    print("🚀 ORACLE SAMUEL ENHANCED FEATURES TEST")
    print("=" * 50)
    
    # Create sample data
    df = create_sample_data()
    print(f"✓ Created sample dataset with {len(df)} properties")
    
    # Test K-means clustering
    kmeans_model, clusters, cluster_analysis = test_kmeans_clustering(df)
    
    # Test logistic regression
    log_reg_model, confusion_matrix, accuracy = test_logistic_regression(df)
    
    # Test enhanced prediction
    prediction_result = test_enhanced_prediction(df, kmeans_model, log_reg_model)
    
    # Create visualizations
    fig = create_visualizations(df)
    
    # Summary
    print("\n" + "=" * 50)
    print("✅ ENHANCED FEATURES TEST COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print(f"✓ K-means clustering: {len(np.unique(clusters))} clusters identified")
    print(f"✓ Logistic regression: {accuracy:.3f} classification accuracy")
    print(f"✓ Enhanced prediction: Cluster {prediction_result['cluster']}, Category {prediction_result['category']}")
    print("✓ Visualizations created and saved")
    
    print("\n🎯 Your Oracle Samuel model now includes:")
    print("  • K-means clustering for market segmentation")
    print("  • Confusion matrix analysis for classification accuracy")
    print("  • Logistic regression for price category prediction")
    print("  • Enhanced visualizations and reporting")
    
    return df, kmeans_model, log_reg_model

if __name__ == "__main__":
    df, kmeans, log_reg = main()
