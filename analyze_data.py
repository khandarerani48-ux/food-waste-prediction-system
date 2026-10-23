import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("data/food_wastage_data.csv")


# ==============================
# BASIC STATISTICS
# ==============================

print("\n========== BASIC STATISTICS ==========")

print("Average Food Waste:",
      round(data["Wastage Food Amount"].mean(), 2))

print("Minimum Food Waste:",
      data["Wastage Food Amount"].min())

print("Maximum Food Waste:",
      data["Wastage Food Amount"].max())


# ==============================
# FOOD TYPE ANALYSIS
# ==============================

food_waste = data.groupby("Type of Food")[
    "Wastage Food Amount"
].mean().sort_values(ascending=False)

print("\n========== AVERAGE WASTE BY FOOD TYPE ==========")
print(food_waste)


# ==============================
# EVENT TYPE ANALYSIS
# ==============================

event_waste = data.groupby("Event Type")[
    "Wastage Food Amount"
].mean().sort_values(ascending=False)

print("\n========== AVERAGE WASTE BY EVENT TYPE ==========")
print(event_waste)


# ==============================
# STORAGE CONDITION ANALYSIS
# ==============================

storage_waste = data.groupby("Storage Conditions")[
    "Wastage Food Amount"
].mean().sort_values(ascending=False)

print("\n========== AVERAGE WASTE BY STORAGE CONDITION ==========")
print(storage_waste)


# ==============================
# CORRELATION
# ==============================

print("\n========== NUMERICAL CORRELATION ==========")

print(
    data[
        ["Number of Guests",
         "Quantity of Food",
         "Wastage Food Amount"]
    ].corr()
)


# ==============================
# VISUALIZATION
# ==============================

food_waste.plot(kind="bar")

plt.title("Average Food Waste by Food Type")
plt.xlabel("Food Type")
plt.ylabel("Average Wastage")

plt.tight_layout()
plt.show()