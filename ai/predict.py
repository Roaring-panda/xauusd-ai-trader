import logging
import numpy as np
from train_model import AITrader

logger = logging.getLogger(__name__)

class Predictor:
    """
    Make predictions using trained AI model
    """
    
    def __init__(self, model_path=None):
        self.trader = AITrader()
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path):
        """
        Load pre-trained model
        
        Args:
            model_path: Path to saved model
        """
        try:
            import pickle
            with open(model_path, 'rb') as f:
                self.trader.model = pickle.load(f)
            logger.info(f"Model loaded from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
    
    def save_model(self, model_path):
        """
        Save trained model
        
        Args:
            model_path: Path to save model
        """
        try:
            import pickle
            with open(model_path, 'wb') as f:
                pickle.dump(self.trader.model, f)
            logger.info(f"Model saved to {model_path}")
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
    
    def predict_signal(self, features):
        """
        Predict trading signal
        
        Args:
            features: Scaled features
        
        Returns:
            dict: Signal and confidence
        """
        if self.trader.model is None:
            return {"signal": 0, "confidence": 0}
        
        prediction = self.trader.predict(features)
        probabilities = self.trader.predict_proba(features)
        
        signal = prediction[0]
        confidence = np.max(probabilities[0])
        
        return {
            "signal": signal,
            "confidence": confidence
        }
