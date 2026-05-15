import numpy as np
from PIL import Image
import os
import hashlib

class SoilAnalyzer:
    def __init__(self):
        # Try both possible model paths
        model_paths = [
            os.path.join(os.path.dirname(__file__), '..', 'models', 'models', 'soil_model.h5'),
            os.path.join(os.path.dirname(__file__), '..', 'models', 'soil_classifier.h5'),
            os.path.join(os.path.dirname(__file__), '..', 'models', 'soil_model.h5'),
        ]
        
        # Try to load TensorFlow model, fall back to mock if not available
        self.model = None
        self.use_mock = False
        self.model_path = None
        
        try:
            try:
                import tensorflow as tf
                keras = tf.keras
            except AttributeError:
                # Fallback for older TensorFlow versions or different installations
                try:
                    import keras
                except ImportError:
                    raise ImportError("Neither tensorflow.keras nor standalone keras available")
            
            # Try each path until one exists
            for path in model_paths:
                if os.path.exists(path):
                    try:
                        self.model = keras.models.load_model(path)
                        self.model_path = path
                        print(f"✅ Model loaded successfully from: {path}")
                        break
                    except Exception as e:
                        print(f"⚠️  Could not load model from {path}: {e}")
                        continue
            
            if self.model is None:
                print(f"⚠️  Warning: Model file not found at any of these locations: {model_paths}. Using mock predictions.")
                self.use_mock = True
                
        except ImportError:
            print("⚠️  Warning: TensorFlow/Keras not available. Using mock predictions.")
            self.use_mock = True
        except Exception as e:
            print(f"⚠️  Warning: Could not load model ({str(e)}). Using mock predictions.")
            self.use_mock = True
            
        self.classes = ['chalky', 'clay', 'loamy', 'peaty', 'sandy', 'silty']
        self.properties = {
            "loamy": {
                "pH_range": "6.0 - 7.0",
                "drainage": "Good",
                "nutrient_retention": "High",
                "workability": "Easy",
                "water_holding": "Moderate to High",
                "color": "Dark brown",
                "texture": "Smooth, partly gritty"
            },
            "sandy": {
                "pH_range": "5.5 - 7.0",
                "drainage": "Excessive",
                "nutrient_retention": "Low",
                "workability": "Very Easy",
                "water_holding": "Low",
                "color": "Light brown/tan",
                "texture": "Gritty, coarse"
            },
            "clay": {
                "pH_range": "6.0 - 8.0",
                "drainage": "Poor",
                "nutrient_retention": "Very High",
                "workability": "Difficult when wet",
                "water_holding": "Very High",
                "color": "Red/brown/grey",
                "texture": "Sticky, smooth"
            },
            "silty": {
                "pH_range": "6.0 - 7.0",
                "drainage": "Moderate",
                "nutrient_retention": "Moderate to High",
                "workability": "Moderate",
                "water_holding": "High",
                "color": "Dark brown",
                "texture": "Silky, flour-like"
            },
            "peaty": {
                "pH_range": "3.5 - 5.5",
                "drainage": "Poor (waterlogged)",
                "nutrient_retention": "High",
                "workability": "Easy when drained",
                "water_holding": "Very High",
                "color": "Very dark/black",
                "texture": "Spongy, fibrous"
            },
            "chalky": {
                "pH_range": "7.5 - 8.5",
                "drainage": "Good to Excessive",
                "nutrient_retention": "Low",
                "workability": "Moderate",
                "water_holding": "Low to Moderate",
                "color": "Pale white/grey",
                "texture": "Stony, gritty"
            }
        }

    def predict(self, image_path):
        """Predict soil type from image"""
        try:
            # Load and preprocess image
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            img = Image.open(image_path).convert('RGB')
            img = img.resize((224, 224))
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            if self.use_mock:
                # Generate mock predictions based on image hash for consistency
                img_hash = hashlib.md5(img_array.tobytes()).hexdigest()
                hash_value = int(img_hash[:8], 16)
                
                # Use hash to select a class and confidence
                predicted_index = hash_value % len(self.classes)
                predicted_class = self.classes[predicted_index]
                
                # Generate confidence between 0.75 and 0.95
                confidence = 0.75 + (hash_value % 20) / 100
                
                # Generate all predictions
                predictions = np.random.random(len(self.classes))
                predictions[predicted_index] = confidence
                predictions = predictions / predictions.sum()
            else:
                # Make prediction with real model
                predictions = self.model.predict(img_array, verbose=0)
                predicted_index = np.argmax(predictions[0])
                predicted_class = self.classes[predicted_index]
                confidence = float(predictions[0][predicted_index])

            # Get all class probabilities - ensure all values are Python floats, not numpy
            all_predictions = {
                self.classes[i]: round(float(predictions[i] if self.use_mock else predictions[0][i]) * 100, 2)
                for i in range(len(self.classes))
            }
            
            # Ensure confidence is a Python float
            predicted_confidence = float(confidence)

            return {
                "soil_type": predicted_class,
                "confidence": round(predicted_confidence, 4),
                "confidence_percent": round(predicted_confidence * 100, 2),
                "properties": self.properties.get(predicted_class, {}),
                "all_predictions": all_predictions,
                "predictions": all_predictions  # Add this for backward compatibility
            }
        except Exception as e:
            print(f"❌ Error in predict: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

# Singleton instance
analyzer = SoilAnalyzer()
