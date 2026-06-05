import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import logging

logger = logging.getLogger(__name__)

class AITrader:
    """
    AI model for XAUUSD price prediction
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
    
    def prepare_features(self, df):
        """
        Prepare features for model training
        
        Features include:
        - Open, High, Low, Close, Volume
        - RSI, MACD, EMA50, EMA200
        
        Args:
            df: DataFrame with OHLC data and indicators
        
        Returns:
            np.ndarray: Scaled features
        """
        feature_cols = ['open', 'high', 'low', 'close', 'tick_volume',
                       'rsi', 'macd', 'signal', 'ema50', 'ema200']
        
        features = df[feature_cols].fillna(0).values
        return self.scaler.fit_transform(features)
    
    def train(self, X_train, y_train):
        """
        Train XGBoost model
        
        Args:
            X_train: Training features
            y_train: Training labels (1=BUY, 0=HOLD, -1=SELL)
        """
        try:
            self.model = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )
            self.model.fit(X_train, y_train)
            logger.info("Model trained successfully")
        except Exception as e:
            logger.error(f"Training error: {e}")
    
    def predict(self, X):
        """
        Make predictions
        
        Args:
            X: Features to predict
        
        Returns:
            np.ndarray: Predictions
        """
        if self.model is None:
            logger.error("Model not trained yet")
            return None
        
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """
        Get prediction probabilities
        
        Args:
            X: Features to predict
        
        Returns:
            np.ndarray: Prediction probabilities
        """
        if self.model is None:
            logger.error("Model not trained yet")
            return None
        
        return self.model.predict_proba(X)
