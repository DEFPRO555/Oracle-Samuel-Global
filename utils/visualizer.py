# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – The Real Estate Market Prophet
# MD5-Protected AI System. Unauthorized use prohibited.

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class RealEstateVisualizer:
    def __init__(self, df):
        self.df = df
        # Set style
        sns.set_style("whitegrid")
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def plot_price_distribution(self, price_col):
        """Plot price distribution histogram"""
        fig = px.histogram(
            self.df,
            x=price_col,
            nbins=50,
            title=f'Price Distribution',
            labels={price_col: 'Price'},
            color_discrete_sequence=['#10b981']
        )
        fig.update_layout(
            template='plotly_white',
            showlegend=False
        )
        return fig
    
    def plot_correlation_heatmap(self):
        """Create correlation heatmap"""
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) < 2:
            return None
        
        corr_matrix = numeric_df.corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdYlGn',
            zmid=0
        ))
        
        fig.update_layout(
            title='Feature Correlation Heatmap',
            template='plotly_white',
            width=800,
            height=800
        )
        return fig
    
    def plot_scatter(self, x_col, y_col, color_col=None):
        """Create scatter plot"""
        fig = px.scatter(
            self.df,
            x=x_col,
            y=y_col,
            color=color_col,
            title=f'{y_col} vs {x_col}',
            labels={x_col: x_col.replace('_', ' ').title(), 
                   y_col: y_col.replace('_', ' ').title()},
            color_continuous_scale='Viridis'
        )
        fig.update_layout(template='plotly_white')
        return fig
    
    def plot_feature_importance(self, feature_importance_df):
        """Plot feature importance"""
        fig = px.bar(
            feature_importance_df.head(10),
            x='importance',
            y='feature',
            orientation='h',
            title='Top 10 Feature Importance',
            labels={'importance': 'Importance Score', 'feature': 'Feature'},
            color='importance',
            color_continuous_scale='tealgrn'
        )
        fig.update_layout(
            template='plotly_white',
            yaxis={'categoryorder': 'total ascending'}
        )
        return fig
    
    def plot_actual_vs_predicted(self, y_test, y_pred):
        """Plot actual vs predicted prices"""
        results_df = pd.DataFrame({
            'Actual': y_test,
            'Predicted': y_pred
        })
        
        fig = px.scatter(
            results_df,
            x='Actual',
            y='Predicted',
            title='Actual vs Predicted Prices',
            labels={'Actual': 'Actual Price', 'Predicted': 'Predicted Price'},
            color_discrete_sequence=['#10b981']
        )
        
        # Add diagonal line
        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())
        fig.add_trace(go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            name='Perfect Prediction',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(template='plotly_white')
        return fig
    
    def plot_residuals(self, y_test, y_pred):
        """Plot residuals"""
        residuals = y_test - y_pred
        
        fig = px.scatter(
            x=y_pred,
            y=residuals,
            title='Residual Plot',
            labels={'x': 'Predicted Values', 'y': 'Residuals'},
            color_discrete_sequence=['#10b981']
        )
        
        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        fig.update_layout(template='plotly_white')
        return fig
    
    def create_summary_metrics(self, metrics_dict):
        """Create summary metrics visualization"""
        fig = go.Figure()
        
        metrics_data = [
            ['MAE', f"${metrics_dict.get('mae', 0):,.0f}"],
            ['RMSE', f"${metrics_dict.get('rmse', 0):,.0f}"],
            ['R² Score', f"{metrics_dict.get('r2_score', 0):.4f}"],
            ['Model', metrics_dict.get('model_type', 'N/A').replace('_', ' ').title()]
        ]
        
        fig.add_trace(go.Table(
            header=dict(
                values=['<b>Metric</b>', '<b>Value</b>'],
                fill_color='#10b981',
                font=dict(color='white', size=14),
                align='left'
            ),
            cells=dict(
                values=list(zip(*metrics_data)),
                fill_color='lavender',
                font=dict(size=12),
                align='left'
            )
        ))
        
        fig.update_layout(
            title='Model Performance Metrics',
            height=300
        )
        return fig
    
    def plot_box_plot(self, column, group_by=None):
        """Create box plot"""
        if group_by:
            fig = px.box(
                self.df,
                x=group_by,
                y=column,
                title=f'{column} Distribution by {group_by}',
                color=group_by,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
        else:
            fig = px.box(
                self.df,
                y=column,
                title=f'{column} Distribution',
                color_discrete_sequence=['#10b981']
            )
        
        fig.update_layout(template='plotly_white')
        return fig

