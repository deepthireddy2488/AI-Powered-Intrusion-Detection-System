from app.ml.load_model import random_forest_model

print("Model Loaded Successfully!")
print(type(random_forest_model))

print("\nFeature Names:")
print(random_forest_model.feature_names_in_)