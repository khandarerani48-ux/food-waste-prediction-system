import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# ==============================
# 1. LOAD DATASET
# ==============================

data = pd.read_csv("data/food_wastage_data.csv")


# ==============================
# 2. FEATURES AND TARGET
# ==============================

X = data.drop("Wastage Food Amount", axis=1)
y = data["Wastage Food Amount"]


# ==============================
# 3. COLUMN TYPES
# ==============================

categorical_columns = [
    "Type of Food",
    "Event Type",
    "Storage Conditions",
    "Purchase History",
    "Seasonality",
    "Preparation Method",
    "Geographical Location",
    "Pricing"
]

numerical_columns = [
    "Number of Guests",
    "Quantity of Food"
]


# ==============================
# 4. PREPROCESSING
# ==============================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_columns
        )
    ],
    remainder="passthrough"
)


# ==============================
# 5. MODEL
# ==============================

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)


# ==============================
# 6. PIPELINE
# ==============================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ==============================
# 7. TRAIN-TEST SPLIT
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ==============================
# 8. TRAIN MODEL
# ==============================

pipeline.fit(X_train, y_train)


# ==============================
# 9. EVALUATE MODEL
# ==============================

predictions = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\n========== FINAL MODEL ==========")
print("Model: Random Forest Regressor")
print("MAE:", round(mae, 2))
print("R² Score:", round(r2, 2))


# ==============================
# 10. SAVE MODEL
# ==============================

joblib.dump(
    pipeline,
    "model/food_waste_model.pkl"
)

print("\nModel saved successfully!")
print("Location: model/food_waste_model.pkl")