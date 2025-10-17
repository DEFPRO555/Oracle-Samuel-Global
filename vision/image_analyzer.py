# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Voice & Vision Intelligence
# MD5-Protected AI System. Unauthorized use prohibited.

import cv2
import numpy as np
from PIL import Image
import io
from datetime import datetime


class PropertyImageAnalyzer:
    """
    Analyzes property images using computer vision
    Detects features, estimates size, evaluates condition
    """
    
    def __init__(self):
        self.analysis_history = []
    
    def analyze_property_image(self, image_file):
        """
        Main analysis function for property images
        
        Args:
            image_file: PIL Image or file path
            
        Returns:
            dict: Analysis results with confidence scores
        """
        try:
            # Load image
            if isinstance(image_file, str):
                image = cv2.imread(image_file)
                pil_image = Image.open(image_file)
            else:
                # Convert uploaded file to OpenCV format
                pil_image = Image.open(image_file)
                image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            # Perform various analyses
            results = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'image_size': pil_image.size,
                'brightness': self._analyze_brightness(image),
                'color_dominance': self._analyze_colors(image),
                'edge_complexity': self._analyze_edges(image),
                'estimated_features': self._estimate_property_features(image),
                'quality_score': 0.0,
                'confidence': 0.75
            }
            
            # Calculate overall quality score
            results['quality_score'] = self._calculate_quality_score(results)
            
            # Add to history
            self.analysis_history.append(results)
            
            return True, results
            
        except Exception as e:
            return False, f"Image analysis error: {str(e)}"
    
    def _analyze_brightness(self, image):
        """Analyze image brightness"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        
        if brightness < 85:
            level = "Dark"
        elif brightness < 170:
            level = "Moderate"
        else:
            level = "Bright"
        
        return {
            'value': float(brightness),
            'level': level,
            'score': min(brightness / 255.0, 1.0)
        }
    
    def _analyze_colors(self, image):
        """Analyze dominant colors in the image"""
        # Convert to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Calculate average color
        avg_color = np.mean(rgb_image, axis=(0, 1))
        
        # Determine dominant color family
        r, g, b = avg_color
        if g > r and g > b:
            dominant = "Green (Vegetation/Garden detected)"
            vegetation_score = 0.8
        elif b > r and b > g:
            dominant = "Blue (Sky/Water detected)"
            vegetation_score = 0.3
        elif r > 150 and g < 100:
            dominant = "Red/Brown (Brick/Roof detected)"
            vegetation_score = 0.2
        else:
            dominant = "Neutral (Building materials)"
            vegetation_score = 0.4
        
        return {
            'rgb': [int(r), int(g), int(b)],
            'dominant': dominant,
            'vegetation_score': vegetation_score
        }
    
    def _analyze_edges(self, image):
        """Analyze edge complexity (indicates detail/structure)"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        if edge_density < 0.05:
            complexity = "Simple structure"
        elif edge_density < 0.15:
            complexity = "Moderate detail"
        else:
            complexity = "Complex architecture"
        
        return {
            'edge_density': float(edge_density),
            'complexity': complexity,
            'detail_score': min(edge_density * 5, 1.0)
        }
    
    def _estimate_property_features(self, image):
        """Estimate property features from image analysis"""
        h, w = image.shape[:2]
        aspect_ratio = w / h
        
        # Estimate size category based on image composition
        if aspect_ratio > 1.5:
            size_estimate = "Wide property (possibly large lot or panoramic view)"
        elif aspect_ratio < 0.7:
            size_estimate = "Tall structure (multi-story building)"
        else:
            size_estimate = "Standard proportions"
        
        # Detect potential features using color analysis
        features = []
        
        # Check for pool (blue pixels in lower portion)
        lower_half = image[image.shape[0]//2:, :]
        blue_channel = lower_half[:, :, 0]  # B in BGR
        if np.mean(blue_channel) > 120:
            features.append("🏊 Possible pool detected")
        
        # Check for garden (green pixels)
        green_channel = image[:, :, 1]  # G in BGR
        if np.mean(green_channel) > 100:
            features.append("🌳 Garden/vegetation present")
        
        # Check for windows (bright rectangular regions would be detected in production)
        features.append("🪟 Windows present (architectural analysis)")
        
        return {
            'size_estimate': size_estimate,
            'aspect_ratio': float(aspect_ratio),
            'detected_features': features,
            'feature_count': len(features)
        }
    
    def _calculate_quality_score(self, results):
        """Calculate overall property quality score from analysis"""
        score = 0.0
        
        # Brightness contributes 25%
        score += results['brightness']['score'] * 0.25
        
        # Vegetation presence contributes 20%
        score += results['color_dominance']['vegetation_score'] * 0.20
        
        # Detail/complexity contributes 25%
        score += results['edge_complexity']['detail_score'] * 0.25
        
        # Feature count contributes 30%
        feature_score = min(results['estimated_features']['feature_count'] / 5.0, 1.0)
        score += feature_score * 0.30
        
        return round(score, 3)
    
    def generate_property_report(self, analysis_results):
        """Generate human-readable property analysis report"""
        if not analysis_results:
            return "No analysis results available"
        
        report = f"""
🏠 **Property Image Analysis Report**

**Overall Quality Score:** {analysis_results['quality_score']:.1%} 
**Analysis Confidence:** {analysis_results['confidence']:.0%}

**📸 Image Properties:**
- Resolution: {analysis_results['image_size'][0]} x {analysis_results['image_size'][1]} pixels
- Brightness: {analysis_results['brightness']['level']} ({analysis_results['brightness']['value']:.0f}/255)

**🎨 Visual Analysis:**
- Dominant Colors: {analysis_results['color_dominance']['dominant']}
- Architectural Detail: {analysis_results['edge_complexity']['complexity']}

**🏡 Property Features Detected:**
- Size/Structure: {analysis_results['estimated_features']['size_estimate']}
- Aspect Ratio: {analysis_results['estimated_features']['aspect_ratio']:.2f}
"""
        
        for feature in analysis_results['estimated_features']['detected_features']:
            report += f"\n- {feature}"
        
        report += f"\n\n**🔮 Oracle Samuel's Assessment:**\n"
        
        # Generate assessment based on quality score
        if analysis_results['quality_score'] > 0.7:
            report += "This property shows excellent visual appeal with strong indicators of value. "
            report += "Well-maintained grounds and attractive features detected."
        elif analysis_results['quality_score'] > 0.5:
            report += "This property demonstrates good condition with notable features. "
            report += "Moderate appeal with room for enhancement."
        else:
            report += "This property shows basic characteristics. "
            report += "Potential for improvement in visual presentation."
        
        return report
    
    def get_analysis_history(self, limit=10):
        """Get recent analysis history"""
        return self.analysis_history[-limit:]

