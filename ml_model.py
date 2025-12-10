"""
Module AI/ML cho dự án ShopAI
Sử dụng Linear Regression để dự đoán thời gian người dùng xem sản phẩm
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import os

class TimePredictor:
    """
    Model dự đoán thời gian người dùng xem trang/sản phẩm
    Sử dụng Linear Regression với UCI Online Shoppers Dataset
    """
    
    def __init__(self, data_file='tracking_data.csv'):
        self.data_file = data_file
        self.model = None
        self.features = ['ProductRelated', 'Administrative', 'Informational', 'PageValues', 'SpecialDay']
        self.is_trained = False
        self.metrics = {}
        
    def prepare_data(self):
        """Chuẩn bị dữ liệu training từ UCI dataset"""
        if not os.path.exists(self.data_file):
            return None, None
            
        df = pd.read_csv(self.data_file)
        
        if len(df) < 10:  # Cần ít nhất 10 samples
            return None, None
        
        # Features từ UCI dataset
        X = df[self.features]
        
        # Target: Tổng thời gian xem trang (ProductRelated_Duration + Administrative_Duration + Informational_Duration)
        y = df['ProductRelated_Duration'] + df['Administrative_Duration'] + df['Informational_Duration']
        
        return X, y
    
    def train(self):
        """Huấn luyện model"""
        X, y = self.prepare_data()
        
        if X is None:
            return False
        
        # Split data: 80% train, 20% test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train Linear Regression
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        
        self.metrics = {
            'mse': round(mean_squared_error(y_test, y_pred), 2),
            'rmse': round(np.sqrt(mean_squared_error(y_test, y_pred)), 2),
            'r2_score': round(r2_score(y_test, y_pred), 3),
            'train_samples': len(X_train),
            'test_samples': len(X_test)
        }
        
        self.is_trained = True
        return True
    
    def predict(self, product_related=5, administrative=1, informational=0, page_values=0, special_day=0):
        """Dự đoán thời gian xem dựa trên UCI features"""
        if not self.is_trained:
            self.train()
        
        if not self.is_trained:
            return 30.0  # Default value
        
        features = [[product_related, administrative, informational, page_values, special_day]]
        
        prediction = self.model.predict(features)[0]
        return max(0, round(prediction, 2))  # Không cho phép giá trị âm
    
    def get_model_info(self):
        """Lấy thông tin model"""
        if not self.is_trained:
            return None
        
        coefficients = {}
        for i, feature in enumerate(self.features):
            coefficients[feature] = round(self.model.coef_[i], 4)
        
        return {
            'algorithm': 'Linear Regression',
            'features': self.features,
            'coefficients': coefficients,
            'intercept': round(self.model.intercept_, 4),
            'metrics': self.metrics
        }
    
    def get_feature_importance(self):
        """Phân tích tầm quan trọng của features"""
        if not self.is_trained:
            return None
        
        importance = {}
        for i, feature in enumerate(self.features):
            importance[feature] = abs(self.model.coef_[i])
        
        total = sum(importance.values())
        importance_percent = {
            k: round((v/total)*100, 1) for k, v in importance.items()
        }
        
        return importance_percent
