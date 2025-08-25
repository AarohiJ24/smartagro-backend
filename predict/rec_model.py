#Model to predict which crop should be grown. accuracy: 99.3% Random Forest
import os,joblib

# Load pre-trained model
# model = joblib.load("models/crop_model.pkl")

# print("Accuracy:", accuracy_score(y_test, y_pred))
# print(classification_report(y_test, y_pred))
BASE = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE, "models", "crop_model.pkl")
model = joblib.load(MODEL_PATH)