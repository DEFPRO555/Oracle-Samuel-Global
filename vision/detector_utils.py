# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Voice & Vision Intelligence
# MD5-Protected AI System. Unauthorized use prohibited.

import cv2
import numpy as np


class PropertyFeatureDetector:
    """
    Utility functions for detecting specific property features
    """
    
    @staticmethod
    def detect_windows(image):
        """Detect potential windows in the image"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        window_candidates = []
        for contour in contours:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h if h > 0 else 0
            
            # Windows typically have aspect ratios between 0.5 and 2.0
            if 0.5 < aspect_ratio < 2.0 and w > 20 and h > 20:
                window_candidates.append({
                    'position': (x, y),
                    'size': (w, h),
                    'aspect_ratio': aspect_ratio
                })
        
        return window_candidates
    
    @staticmethod
    def estimate_building_size(image):
        """Estimate relative building size in image"""
        h, w = image.shape[:2]
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold to separate building from background
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Calculate building coverage
        building_pixels = np.sum(thresh > 0)
        total_pixels = h * w
        coverage = building_pixels / total_pixels
        
        if coverage > 0.6:
            size_category = "Large"
        elif coverage > 0.3:
            size_category = "Medium"
        else:
            size_category = "Small"
        
        return {
            'coverage_percentage': coverage * 100,
            'size_category': size_category,
            'estimated_area_pixels': int(building_pixels)
        }
    
    @staticmethod
    def detect_pool(image):
        """Detect if there's a swimming pool in the image"""
        # Convert to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define range for blue color (typical pool water)
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])
        
        # Create mask for blue regions
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        
        # Calculate blue pixel percentage
        blue_percentage = np.sum(mask > 0) / mask.size
        
        # Pool detected if significant blue area (>2%)
        has_pool = blue_percentage > 0.02
        
        return {
            'has_pool': has_pool,
            'confidence': min(blue_percentage * 50, 1.0),
            'blue_area_percentage': blue_percentage * 100
        }
    
    @staticmethod
    def detect_vegetation(image):
        """Detect vegetation/garden in the image"""
        # Convert to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define range for green color (vegetation)
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        
        # Create mask for green regions
        mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # Calculate green pixel percentage
        green_percentage = np.sum(mask > 0) / mask.size
        
        if green_percentage > 0.3:
            vegetation_level = "Extensive"
        elif green_percentage > 0.15:
            vegetation_level = "Moderate"
        elif green_percentage > 0.05:
            vegetation_level = "Minimal"
        else:
            vegetation_level = "None"
        
        return {
            'vegetation_level': vegetation_level,
            'green_area_percentage': green_percentage * 100,
            'has_garden': green_percentage > 0.15
        }
    
    @staticmethod
    def analyze_roof_condition(image):
        """Analyze roof condition based on visual features"""
        # Focus on top portion of image (where roof typically is)
        height = image.shape[0]
        roof_region = image[:height//3, :]
        
        # Calculate color variance (damaged roofs have higher variance)
        gray_roof = cv2.cvtColor(roof_region, cv2.COLOR_BGR2GRAY)
        variance = np.var(gray_roof)
        
        if variance < 500:
            condition = "Uniform (Good condition)"
        elif variance < 1500:
            condition = "Moderate variance"
        else:
            condition = "High variance (potential damage)"
        
        return {
            'condition': condition,
            'variance': float(variance),
            'estimated_quality': "Good" if variance < 1000 else "Fair" if variance < 2000 else "Poor"
        }

