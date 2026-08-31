from app.ml.load_model import random_forest_model

print("Number of Features:", len(random_forest_model.feature_names_in_))

print("\nFirst 10 Features:")

for feature in random_forest_model.feature_names_in_[:10]:
    print(feature)