import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
data = pd.read_csv("crop_data.csv")

# Encode categorical columns
le_season = LabelEncoder()
le_soil = LabelEncoder()
le_water = LabelEncoder()
le_crop = LabelEncoder()

data["Season"] = le_season.fit_transform(data["Season"])
data["Soil"] = le_soil.fit_transform(data["Soil"])
data["Water"] = le_water.fit_transform(data["Water"])
data["Crop"] = le_crop.fit_transform(data["Crop"])

X = data[["Season", "Soil", "Water"]]
y = data["Crop"]

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model and encoders
joblib.dump({
    "model": model,
    "le_season": le_season,
    "le_soil": le_soil,
    "le_water": le_water,
    "le_crop": le_crop
}, "crop_model.pkl")

print("Crop recommendation model trained and saved as crop_model.pkl")
