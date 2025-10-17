# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Enhanced Features Integration Code
# MD5-Protected AI System. Unauthorized use prohibited.

# Add these imports to the top of your app.py
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler

# Add to session state initialization
if 'enhanced_features' not in st.session_state:
    st.session_state.enhanced_features = {
        'kmeans_model': None,
        'logistic_model': None,
        'clusters': None,
        'price_categories': None,
        'confusion_matrix_data': None,
        'scaler': StandardScaler()
    }

def enhance_with_kmeans_clustering(df, n_clusters=5):
    """Add K-means clustering for market segmentation"""
    st.info("Adding K-means clustering for market segmentation...")
    
    # Prepare numeric features for clustering
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    price_col = None
    for col in numeric_cols:
        if 'price' in col.lower():
            price_col = col
            numeric_cols.remove(col)
            break
    
    if len(numeric_cols) < 2:
        return False, "Insufficient numeric features for clustering"
    
    X_cluster = df[numeric_cols].fillna(0)
    X_scaled = st.session_state.enhanced_features['scaler'].fit_transform(X_cluster)
    
    # Determine optimal number of clusters using elbow method
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
    kmeans_model = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    clusters = kmeans_model.fit_predict(X_scaled)
    
    # Store in session state
    st.session_state.enhanced_features['kmeans_model'] = kmeans_model
    st.session_state.enhanced_features['clusters'] = clusters
    
    # Analyze clusters
    cluster_analysis = {}
    for cluster_id in np.unique(clusters):
        cluster_data = df[clusters == cluster_id]
        if price_col:
            cluster_analysis[cluster_id] = {
                'size': len(cluster_data),
                'avg_price': cluster_data[price_col].mean(),
                'price_std': cluster_data[price_col].std(),
                'price_range': f"${cluster_data[price_col].min():,.0f} - ${cluster_data[price_col].max():,.0f}"
            }
    
    return True, {
        'optimal_clusters': optimal_k,
        'silhouette_score': max(silhouette_scores),
        'cluster_analysis': cluster_analysis
    }

def enhance_with_logistic_regression(df):
    """Add logistic regression for price category classification"""
    st.info("Adding logistic regression for price category classification...")
    
    # Find price column
    price_col = None
    for col in df.columns:
        if 'price' in col.lower():
            price_col = col
            break
    
    if not price_col:
        return False, "No price column found"
    
    # Create price categories based on quartiles
    price_quartiles = np.percentile(df[price_col], [25, 50, 75])
    
    def categorize_price(price):
        if price <= price_quartiles[0]:
            return 'Low'
        elif price <= price_quartiles[1]:
            return 'Medium-Low'
        elif price <= price_quartiles[2]:
            return 'Medium-High'
        else:
            return 'High'
    
    price_categories = df[price_col].apply(categorize_price)
    
    # Prepare features for logistic regression
    feature_cols = [col for col in df.columns if col != price_col]
    X = df[feature_cols].select_dtypes(include=[np.number]).fillna(0)
    
    if len(X.columns) == 0:
        return False, "No suitable features for logistic regression"
    
    # Train logistic regression
    from sklearn.model_selection import train_test_split
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, price_categories, test_size=0.2, random_state=42, stratify=price_categories
    )
    
    logistic_model = LogisticRegression(random_state=42, max_iter=1000)
    logistic_model.fit(X_train, y_train)
    
    # Generate confusion matrix
    y_pred = logistic_model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Store in session state
    st.session_state.enhanced_features['logistic_model'] = logistic_model
    st.session_state.enhanced_features['price_categories'] = price_categories
    st.session_state.enhanced_features['confusion_matrix_data'] = {
        'matrix': cm,
        'accuracy': accuracy,
        'classes': logistic_model.classes_,
        'classification_report': classification_report(y_test, y_pred)
    }
    
    return True, {
        'accuracy': accuracy,
        'confusion_matrix': cm,
        'classes': logistic_model.classes_
    }

def create_enhanced_visualizations(df):
    """Create enhanced visualizations with clustering and confusion matrix"""
    visualizations = {}
    
    # 1. Cluster Analysis Visualization
    if st.session_state.enhanced_features['clusters'] is not None:
        price_col = None
        for col in df.columns:
            if 'price' in col.lower():
                price_col = col
                break
        
        if price_col:
            df_with_clusters = df.copy()
            df_with_clusters['cluster'] = st.session_state.enhanced_features['clusters']
            
            fig_cluster = px.scatter(
                df_with_clusters, 
                x='cluster', 
                y=price_col,
                color='cluster',
                title='Market Clusters by Price',
                labels={'cluster': 'Market Cluster', price_col: 'Price ($)'}
            )
            visualizations['cluster_analysis'] = fig_cluster
    
    # 2. Confusion Matrix Heatmap
    if st.session_state.enhanced_features['confusion_matrix_data'] is not None:
        cm_data = st.session_state.enhanced_features['confusion_matrix_data']
        cm = cm_data['matrix']
        classes = cm_data['classes']
        
        fig_cm = px.imshow(
            cm,
            text_auto=True,
            aspect="auto",
            title=f'Confusion Matrix (Accuracy: {cm_data["accuracy"]:.3f})',
            labels=dict(x="Predicted", y="Actual", color="Count")
        )
        fig_cm.update_xaxes(tickmode='array', tickvals=list(range(len(classes))), ticktext=classes)
        fig_cm.update_yaxes(tickmode='array', tickvals=list(range(len(classes))), ticktext=classes)
        visualizations['confusion_matrix'] = fig_cm
    
    # 3. Price Category Distribution
    if st.session_state.enhanced_features['price_categories'] is not None:
        category_counts = st.session_state.enhanced_features['price_categories'].value_counts()
        fig_categories = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title='Price Category Distribution'
        )
        visualizations['price_categories'] = fig_categories
    
    return visualizations

def generate_enhancement_report():
    """Generate comprehensive enhancement report"""
    report = "ORACLE SAMUEL ENHANCEMENT REPORT\n"
    report += "=" * 50 + "\n\n"
    
    # K-means clustering report
    if st.session_state.enhanced_features['clusters'] is not None:
        report += "K-MEANS CLUSTERING ANALYSIS\n"
        report += "-" * 30 + "\n"
        report += f"Number of clusters: {len(np.unique(st.session_state.enhanced_features['clusters']))}\n"
        report += "\n"
    
    # Logistic regression report
    if st.session_state.enhanced_features['confusion_matrix_data'] is not None:
        cm_data = st.session_state.enhanced_features['confusion_matrix_data']
        report += "LOGISTIC REGRESSION ANALYSIS\n"
        report += "-" * 30 + "\n"
        report += f"Classification Accuracy: {cm_data['accuracy']:.3f}\n"
        report += f"Price Categories: {', '.join(cm_data['classes'])}\n"
        report += f"\nClassification Report:\n{cm_data['classification_report']}\n"
    
    return report

def add_enhanced_features_ui():
    """Add enhanced features UI to existing tabs"""
    
    st.markdown("---")
    st.subheader("Enhanced AI Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Add K-means Clustering", key="kmeans_btn"):
            if st.session_state.cleaned_df is not None:
                success, result = enhance_with_kmeans_clustering(st.session_state.cleaned_df)
                if success:
                    st.success(f"K-means clustering added! {result['optimal_clusters']} clusters found")
                    st.balloons()
                else:
                    st.error(f"{result}")
            else:
                st.warning("Please upload and clean data first")
    
    with col2:
        if st.button("Add Logistic Regression", key="logistic_btn"):
            if st.session_state.cleaned_df is not None:
                success, result = enhance_with_logistic_regression(st.session_state.cleaned_df)
                if success:
                    st.success(f"Logistic regression added! Accuracy: {result['accuracy']:.3f}")
                    st.balloons()
                else:
                    st.error(f"{result}")
            else:
                st.warning("Please upload and clean data first")
    
    with col3:
        if st.button("Generate Enhanced Report", key="report_btn"):
            if st.session_state.enhanced_features['clusters'] is not None or st.session_state.enhanced_features['confusion_matrix_data'] is not None:
                report = generate_enhancement_report()
                st.text(report)
            else:
                st.warning("Please add enhanced features first")
    
    # Show enhanced visualizations
    if st.session_state.cleaned_df is not None:
        visualizations = create_enhanced_visualizations(st.session_state.cleaned_df)
        
        if visualizations:
            st.markdown("### Enhanced Visualizations")
            for viz_name, fig in visualizations.items():
                st.plotly_chart(fig, use_container_width=True)

def predict_with_enhancements(input_data):
    """Enhanced prediction with clustering and category information"""
    if st.session_state.predictor is None:
        return None, "No base predictor available"
    
    try:
        # Get base prediction
        base_prediction, error = st.session_state.predictor.predict_price(input_data)
        if error:
            return None, error
        
        # Get cluster assignment if available
        cluster_info = None
        if st.session_state.enhanced_features['kmeans_model'] is not None:
            # Prepare input for clustering
            numeric_cols = [col for col in input_data.keys() if isinstance(input_data[col], (int, float))]
            if len(numeric_cols) >= 2:
                cluster_input = np.array([[input_data[col] for col in numeric_cols]])
                cluster_input_scaled = st.session_state.enhanced_features['scaler'].transform(cluster_input)
                cluster = st.session_state.enhanced_features['kmeans_model'].predict(cluster_input_scaled)[0]
                cluster_info = f"Market Cluster {cluster}"
        
        # Get price category if available
        category_info = None
        if st.session_state.enhanced_features['logistic_model'] is not None and base_prediction:
            # Create price category based on prediction
            price_quartiles = np.percentile(st.session_state.cleaned_df[[col for col in st.session_state.cleaned_df.columns if 'price' in col.lower()][0]], [25, 50, 75])
            
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
                'kmeans_clustering': st.session_state.enhanced_features['kmeans_model'] is not None,
                'logistic_regression': st.session_state.enhanced_features['logistic_model'] is not None,
                'confusion_matrix': st.session_state.enhanced_features['confusion_matrix_data'] is not None
            }
        }
        
        return enhanced_result, None
        
    except Exception as e:
        return None, f"Enhanced prediction error: {str(e)}"
