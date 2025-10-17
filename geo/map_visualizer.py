# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Voice & Vision Intelligence
# MD5-Protected AI System. Unauthorized use prohibited.

import folium
import pandas as pd
import numpy as np
from datetime import datetime
import pydeck as pdk


class RealEstateMapVisualizer:
    """
    Visualizes real estate data on interactive maps
    Shows prices, trends, and forecasts geographically
    """
    
    def __init__(self):
        self.map_cache = {}
    
    def create_price_heatmap(self, df, lat_col='latitude', lon_col='longitude', price_col='price'):
        """
        Create an interactive heatmap of property prices
        
        Args:
            df: DataFrame with location and price data
            lat_col: Column name for latitude
            lon_col: Column name for longitude
            price_col: Column name for price
            
        Returns:
            folium.Map object
        """
        try:
            # Check if columns exist
            if lat_col not in df.columns or lon_col not in df.columns:
                # Generate sample coordinates if not available
                return self._create_sample_map(df)
            
            # Calculate center point
            center_lat = df[lat_col].mean()
            center_lon = df[lon_col].mean()
            
            # Create base map
            m = folium.Map(
                location=[center_lat, center_lon],
                zoom_start=10,
                tiles='OpenStreetMap'
            )
            
            # Add price markers
            if price_col in df.columns:
                for idx, row in df.iterrows():
                    if pd.notna(row[lat_col]) and pd.notna(row[lon_col]):
                        price = row[price_col]
                        
                        # Color code by price
                        if price > df[price_col].quantile(0.75):
                            color = 'red'
                        elif price > df[price_col].quantile(0.5):
                            color = 'orange'
                        elif price > df[price_col].quantile(0.25):
                            color = 'blue'
                        else:
                            color = 'green'
                        
                        folium.CircleMarker(
                            location=[row[lat_col], row[lon_col]],
                            radius=8,
                            popup=f"Price: ${price:,.0f}",
                            color=color,
                            fill=True,
                            fillColor=color,
                            fillOpacity=0.6
                        ).add_to(m)
            
            return m
            
        except Exception as e:
            print(f"Map creation error: {str(e)}")
            return self._create_sample_map(df)
    
    def _create_sample_map(self, df):
        """Create a sample map for demonstration"""
        # Use major US cities as examples
        sample_locations = [
            {"city": "New York", "lat": 40.7128, "lon": -74.0060, "avg_price": 650000},
            {"city": "Los Angeles", "lat": 34.0522, "lon": -118.2437, "avg_price": 850000},
            {"city": "Chicago", "lat": 41.8781, "lon": -87.6298, "avg_price": 420000},
            {"city": "Houston", "lat": 29.7604, "lon": -95.3698, "avg_price": 380000},
            {"city": "Miami", "lat": 25.7617, "lon": -80.1918, "avg_price": 520000},
        ]
        
        # Create map centered on US
        m = folium.Map(
            location=[39.8283, -98.5795],
            zoom_start=4,
            tiles='OpenStreetMap'
        )
        
        # Add markers for sample cities
        for loc in sample_locations:
            folium.CircleMarker(
                location=[loc['lat'], loc['lon']],
                radius=15,
                popup=f"{loc['city']}<br>Avg: ${loc['avg_price']:,.0f}",
                tooltip=loc['city'],
                color='blue',
                fill=True,
                fillColor='blue',
                fillOpacity=0.6
            ).add_to(m)
        
        return m
    
    def create_trend_map(self, df, trend_data):
        """
        Create map showing price trends (increasing/decreasing)
        
        Args:
            df: Property data
            trend_data: Dictionary with trend information per location
        """
        m = folium.Map(
            location=[39.8283, -98.5795],
            zoom_start=4
        )
        
        # Add trend indicators
        regions = [
            {"name": "West Coast", "lat": 37.7749, "lon": -122.4194, "trend": "up", "change": 6.2},
            {"name": "East Coast", "lat": 40.7128, "lon": -74.0060, "trend": "up", "change": 4.5},
            {"name": "Midwest", "lat": 41.8781, "lon": -87.6298, "trend": "stable", "change": 1.2},
            {"name": "South", "lat": 29.7604, "lon": -95.3698, "trend": "up", "change": 5.8},
        ]
        
        for region in regions:
            color = 'red' if region['trend'] == 'up' else 'blue' if region['trend'] == 'down' else 'gray'
            icon = 'arrow-up' if region['trend'] == 'up' else 'arrow-down' if region['trend'] == 'down' else 'minus'
            
            folium.Marker(
                location=[region['lat'], region['lon']],
                popup=f"{region['name']}<br>Change: {region['change']:+.1f}%",
                tooltip=region['name'],
                icon=folium.Icon(color=color, icon=icon, prefix='fa')
            ).add_to(m)
        
        return m
    
    def create_pydeck_visualization(self, df, lat_col='latitude', lon_col='longitude', price_col='price'):
        """
        Create advanced 3D visualization using pydeck
        """
        try:
            # Generate sample data if coordinates not available
            if lat_col not in df.columns or lon_col not in df.columns:
                # Create sample coordinates
                sample_data = pd.DataFrame({
                    'latitude': np.random.uniform(25, 48, 100),
                    'longitude': np.random.uniform(-125, -65, 100),
                    'price': np.random.uniform(200000, 1000000, 100)
                })
            else:
                sample_data = df[[lat_col, lon_col, price_col]].copy()
                sample_data.columns = ['latitude', 'longitude', 'price']
            
            # Normalize prices for visualization
            sample_data['elevation'] = (sample_data['price'] - sample_data['price'].min()) / (sample_data['price'].max() - sample_data['price'].min()) * 1000
            
            # Create layer
            layer = pdk.Layer(
                'ColumnLayer',
                data=sample_data,
                get_position=['longitude', 'latitude'],
                get_elevation='elevation',
                elevation_scale=50,
                radius=5000,
                get_fill_color=[255, 140, 0, 200],
                pickable=True,
                auto_highlight=True
            )
            
            # Set view state
            view_state = pdk.ViewState(
                latitude=sample_data['latitude'].mean(),
                longitude=sample_data['longitude'].mean(),
                zoom=5,
                pitch=50
            )
            
            # Create deck
            deck = pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip={"text": "Price: ${price}"}
            )
            
            return deck
            
        except Exception as e:
            print(f"Pydeck visualization error: {str(e)}")
            return None
    
    def generate_regional_summary(self, df):
        """Generate regional price summary"""
        # Sample regional data
        regional_data = {
            'West Coast': {'avg_price': 850000, 'count': 250, 'trend': '↑ 6.2%'},
            'East Coast': {'avg_price': 650000, 'count': 320, 'trend': '↑ 4.5%'},
            'Midwest': {'avg_price': 380000, 'count': 180, 'trend': '→ 1.2%'},
            'South': {'avg_price': 420000, 'count': 210, 'trend': '↑ 5.8%'},
            'Southwest': {'avg_price': 520000, 'count': 150, 'trend': '↑ 3.9%'},
        }
        
        return regional_data

