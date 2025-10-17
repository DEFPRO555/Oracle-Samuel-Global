# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Voice & Vision Intelligence
# MD5-Protected AI System. Unauthorized use prohibited.

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class GeoForecastEngine:
    """
    Geographical price forecasting engine
    Predicts regional price trends and growth
    """
    
    def __init__(self):
        self.forecast_cache = {}
        self.regional_models = {}
    
    def generate_regional_forecast(self, df, months_ahead=12):
        """
        Generate price forecasts for different regions
        
        Args:
            df: Property data DataFrame
            months_ahead: Number of months to forecast
            
        Returns:
            dict: Regional forecasts
        """
        try:
            # Define major regions (sample data for demonstration)
            regions = {
                'Northeast': {'base_price': 650000, 'growth_rate': 0.045},
                'Southeast': {'base_price': 420000, 'growth_rate': 0.058},
                'Midwest': {'base_price': 380000, 'growth_rate': 0.012},
                'Southwest': {'base_price': 520000, 'growth_rate': 0.039},
                'West': {'base_price': 850000, 'growth_rate': 0.062},
            }
            
            forecasts = {}
            
            for region, data in regions.items():
                base_price = data['base_price']
                annual_growth = data['growth_rate']
                monthly_growth = (1 + annual_growth) ** (1/12) - 1
                
                # Generate monthly forecasts
                forecast_prices = []
                current_price = base_price
                
                for month in range(months_ahead + 1):
                    forecast_prices.append({
                        'month': month,
                        'date': (datetime.now() + timedelta(days=30*month)).strftime('%Y-%m'),
                        'price': round(current_price, 2)
                    })
                    current_price *= (1 + monthly_growth)
                
                forecasts[region] = {
                    'forecast_data': forecast_prices,
                    'annual_growth': annual_growth * 100,
                    'price_range': {
                        'current': base_price,
                        'forecast_12m': forecast_prices[-1]['price']
                    }
                }
            
            return forecasts
            
        except Exception as e:
            print(f"Forecast generation error: {str(e)}")
            return {}
    
    def predict_hotspot_regions(self, forecast_data):
        """
        Identify regions with highest growth potential
        
        Args:
            forecast_data: Regional forecast dictionary
            
        Returns:
            list: Sorted list of regions by growth potential
        """
        hotspots = []
        
        for region, data in forecast_data.items():
            growth = data['annual_growth']
            hotspots.append({
                'region': region,
                'growth_rate': growth,
                'current_price': data['price_range']['current'],
                'forecast_price': data['price_range']['forecast_12m']
            })
        
        # Sort by growth rate
        hotspots.sort(key=lambda x: x['growth_rate'], reverse=True)
        
        return hotspots
    
    def calculate_investment_score(self, region_data, affordability_weight=0.3, growth_weight=0.7):
        """
        Calculate investment attractiveness score for a region
        
        Args:
            region_data: Data for a specific region
            affordability_weight: Weight for affordability (0-1)
            growth_weight: Weight for growth potential (0-1)
        """
        # Normalize prices (lower is better for affordability)
        max_price = 1000000
        affordability_score = 1 - (region_data['current_price'] / max_price)
        
        # Growth rate score (higher is better)
        max_growth = 10.0  # 10% annual growth
        growth_score = min(region_data['growth_rate'] / max_growth, 1.0)
        
        # Calculate weighted score
        investment_score = (affordability_score * affordability_weight + 
                           growth_score * growth_weight)
        
        return round(investment_score * 100, 2)
    
    def generate_market_outlook(self, forecasts):
        """Generate textual market outlook based on forecasts"""
        hotspots = self.predict_hotspot_regions(forecasts)
        
        outlook = f"**📊 Market Outlook Report - {datetime.now().strftime('%B %Y')}**\n\n"
        
        outlook += "**🔥 Top Growth Markets:**\n"
        for idx, spot in enumerate(hotspots[:3], 1):
            outlook += f"{idx}. **{spot['region']}** - {spot['growth_rate']:.1f}% annual growth\n"
            outlook += f"   Current Avg: ${spot['current_price']:,.0f} → Forecast: ${spot['forecast_price']:,.0f}\n"
        
        outlook += "\n**📈 Market Sentiment:**\n"
        
        avg_growth = np.mean([h['growth_rate'] for h in hotspots])
        
        if avg_growth > 5.0:
            sentiment = "🟢 **Strong Bullish** - Robust growth across most regions"
        elif avg_growth > 3.0:
            sentiment = "🟡 **Moderately Bullish** - Steady growth with regional variations"
        elif avg_growth > 1.0:
            sentiment = "🟠 **Neutral** - Stable market with selective opportunities"
        else:
            sentiment = "🔴 **Cautious** - Limited growth, focus on fundamentals"
        
        outlook += f"{sentiment}\n\n"
        
        outlook += f"**🎯 Oracle Samuel's Recommendation:**\n"
        best_region = hotspots[0]
        outlook += f"Focus investment attention on the **{best_region['region']}** region, "
        outlook += f"which shows the strongest growth trajectory at {best_region['growth_rate']:.1f}% annually. "
        outlook += "This market demonstrates exceptional momentum and value appreciation potential."
        
        return outlook
    
    def export_forecast_data(self, forecasts, format='dataframe'):
        """Export forecast data in various formats"""
        if format == 'dataframe':
            # Combine all regional forecasts into single DataFrame
            all_data = []
            
            for region, data in forecasts.items():
                for point in data['forecast_data']:
                    all_data.append({
                        'region': region,
                        'month': point['month'],
                        'date': point['date'],
                        'price': point['price'],
                        'growth_rate': data['annual_growth']
                    })
            
            return pd.DataFrame(all_data)
        
        return forecasts

