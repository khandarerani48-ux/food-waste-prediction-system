
import html

import joblib
import pandas as pd
import streamlit as st

from datetime import datetime
from pathlib import Path


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Food Waste Prediction System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>
    .stApp {
        background-color: #f4f7fb;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 1rem;
    }

    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    .header-box {
        background: linear-gradient(135deg, #173b5e, #287b78);
        padding: 28px 30px;
        border-radius: 16px;
        margin-bottom: 24px;
    }

    .header-title {
        color: white;
        font-size: 29px;
        font-weight: 800;
        margin: 0;
    }

    .header-subtitle {
        color: #e1eff5;
        font-size: 14px;
        margin-top: 8px;
    }

    
.section-title {
    color: #19385a;
    font-size: 17px;
    font-weight: 700;
    margin-top: 12px;
    margin-bottom: 12px;
}


    .input-card, .metric-card {
        background: white;
        border: 1px solid #e1e8ef;
        border-radius: 12px;
        padding: 14px;
        min-height: 76px;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(20, 40, 60, 0.035);
    }

    .input-label, .metric-label {
        color: #718096;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        margin-bottom: 7px;
    }

    .input-value {
        color: #19385a;
        font-size: 14px;
        font-weight: 700;
        overflow-wrap: anywhere;
    }

    .metric-value {
        color: #19385a;
        font-size: 22px;
        font-weight: 800;
        overflow-wrap: anywhere;
    }

    .metric-description {
        color: #8492a1;
        font-size: 11px;
        margin-top: 5px;
    }

    .result-box {
        background: white;
        border: 1px solid #dce6ee;
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(20, 40, 60, 0.045);
    }

    .result-label {
        color: #718096;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.7px;
    }

    .result-number {
        color: #173b5e;
        font-size: 43px;
        font-weight: 850;
        margin: 8px 0 2px;
    }

    .result-unit {
        color: #8492a1;
        font-size: 12px;
    }

    .recommendation-box {
        background: #eff8f2;
        border: 1px solid #c6e5d0;
        border-radius: 15px;
        padding: 20px;
        margin-top: 12px;
    }

    .recommendation-title {
        color: #19703b;
        font-size: 17px;
        font-weight: 750;
    }

    .recommendation-text {
        color: #486351;
        font-size: 13px;
        line-height: 1.7;
        margin-top: 8px;
    }

    .risk-low {
        color: #16803d;
        font-weight: 800;
    }

    .risk-moderate {
        color: #a16207;
        font-weight: 800;
    }

    .risk-high {
        color: #c0392b;
        font-weight: 800;
    }

    .footer {
        text-align: center;
        color: #8793a0;
        font-size: 12px;
        padding: 18px 5px;
    }

    .stButton > button {
        width: 100%;
        min-height: 45px;
        border-radius: 9px;
        font-weight: 700;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)



# =========================================================
# PROFESSIONAL DASHBOARD THEME
# =========================================================

st.markdown("""
<style>
/* Main background */
.stApp {
    background-color: #F4F7FC;
}

/* Main content spacing */
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}

/* Main headings */
h1 {
    color: #123B67 !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #174A7E !important;
    font-weight: 700 !important;
}

/* Section headings */
.section-title {
    color: #174A7E;
    font-size: 1.35rem;
    font-weight: 750;
    padding: 12px 0;
    margin: 12px 0;
    border-bottom: 2px solid #D7E5F5;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #EAF2FC;
    border-right: 1px solid #D5E2F2;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #123B67 !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE6F2;
    border-radius: 14px;
    padding: 18px 16px;
    box-shadow: 0 3px 12px rgba(25, 65, 110, 0.06);
}

[data-testid="stMetricLabel"] {
    color: #52677F !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #174A7E !important;
    font-weight: 800;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    background-color: #1769AA;
    color: #FFFFFF;
    border: none;
    border-radius: 9px;
    padding: 0.55rem 1rem;
    font-weight: 650;
    transition: 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #104C80;
    color: #FFFFFF;
    border: none;
}

/* Input fields */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] div[data-baseweb="select"] {
    border-radius: 8px;
}

/* Forms and bordered containers */
[data-testid="stForm"],
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 12px;
}

/* Charts and data tables */
[data-testid="stVegaLiteChart"],
[data-testid="stArrowVegaLiteChart"],
[data-testid="stDataFrame"] {
    background-color: #FFFFFF;
    border: 1px solid #E0E8F2;
    border-radius: 12px;
    padding: 8px;
}

/* Info and success messages */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Horizontal dividers */
hr {
    border-color: #DCE6F2;
}

/* Footer */
.custom-footer {
    text-align: center;
    color: #6B7F95;
    font-size: 0.85rem;
    padding: 20px 0 5px;
}
</style>
""", unsafe_allow_html=True)



# =========================================================
# LOAD MODEL AND DATASET
# =========================================================

try:
    model = joblib.load("model/food_waste_model.pkl")
    data = pd.read_csv("data/food_wastage_data.csv")

    required_columns = [
        "Type of Food",
        "Number of Guests",
        "Event Type",
        "Quantity of Food",
        "Storage Conditions",
        "Purchase History",
        "Seasonality",
        "Preparation Method",
        "Geographical Location",
        "Pricing",
        "Wastage Food Amount"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in data.columns
    ]

    if missing_columns:
        st.error(
            "The dataset is missing required columns: "
            + ", ".join(missing_columns)
        )
        st.stop()

except Exception as e:
    st.error("Unable to load the model or dataset.")
    st.code(str(e))
    st.stop()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def input_card(label, value):
    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))

    st.markdown(
        f"""
        <div class="input-card">
            <div class="input-label">{safe_label}</div>
            <div class="input-value">{safe_value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def metric_card(label, value, description=""):
    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))
    safe_description = html.escape(str(description))

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{safe_label}</div>
            <div class="metric-value">{safe_value}</div>
            <div class="metric-description">{safe_description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="header-box">
    <div class="header-title">
        🍽️ Food Waste Prediction System
    </div>
    <div class="header-subtitle">
        An intelligent machine learning dashboard for
        food waste estimation and preparation planning.
    </div>
</div>
""", unsafe_allow_html=True)

def clear_prediction_inputs():
    keys_to_clear = [
        "food_type",
        "quantity_of_food",
        "preparation_method",
        "number_of_guests",
        "event_type",
        "seasonality",
        "storage_conditions",
        "purchase_history",
        "geographical_location",
        "pricing"
    ]

    for key in keys_to_clear:
        st.session_state[key] = None

# =========================================================
# SIDEBAR INPUT FORM
# =========================================================

with st.sidebar:

    st.markdown("## 🔮 Predict Food Waste")

    st.caption(
        "Enter the food, event and storage details "
        "to estimate expected food waste."
    )

with st.sidebar:
    st.markdown("## 🔮 Predict Food Waste")

    with st.form("prediction_form",  enter_to_submit=False):

        st.markdown("### 🍽️ Food Details")

        food_type = st.selectbox(
            "Type of Food",
            options=sorted(data["Type of Food"].dropna().unique()),
            index=None,
            placeholder="Select food type",
            key="food_type"
        )

        quantity_of_food = st.number_input(
            "Quantity of Food",
            min_value=1,
            value=None,
            step=1,
            placeholder="Enter quantity",
            key="quantity_of_food"
        )

        preparation_method = st.selectbox(
            "Preparation Method",
            options=sorted(
                data["Preparation Method"].dropna().unique()
            ),
            index=None,
            placeholder="Select preparation method",
            key="preparation_method"
        )

        st.markdown("### 👥 Event Details")

        number_of_guests = st.number_input(
            "Number of Guests",
            min_value=1,
            value=None,
            step=1,
            placeholder="Enter number of guests",
            key="number_of_guests"
        )

        event_type = st.selectbox(
            "Event Type",
            options=sorted(data["Event Type"].dropna().unique()),
            index=None,
            placeholder="Select event type",
            key="event_type"
        )

        seasonality = st.selectbox(
            "Seasonality",
            options=sorted(data["Seasonality"].dropna().unique()),
            index=None,
            placeholder="Select season",
            key="seasonality"
        )

        st.markdown("### 📦 Storage & Business")

        storage_conditions = st.selectbox(
            "Storage Conditions",
            options=sorted(
                data["Storage Conditions"].dropna().unique()
            ),
            index=None,
            placeholder="Select storage condition",
            key="storage_conditions"
        )

        purchase_history = st.selectbox(
            "Purchase History",
            options=sorted(
                data["Purchase History"].dropna().unique()
            ),
            index=None,
            placeholder="Select purchase history",
            key="purchase_history"
        )

        geographical_location = st.selectbox(
            "Geographical Location",
            options=sorted(
                data["Geographical Location"].dropna().unique()
            ),
            index=None,
            placeholder="Select location",
            key="geographical_location"
        )

        pricing = st.selectbox(
            "Pricing",
            options=sorted(data["Pricing"].dropna().unique()),
            index=None,
            placeholder="Select pricing",
            key="pricing"
        )

        st.divider()

        # This button MUST remain inside the form.
        predict_button = st.form_submit_button(
            "🔮 Predict Food Waste",
            type="primary",
            use_container_width=True
        )

# =========================================================
# PREDICTION AND DASHBOARD
# =========================================================

if predict_button:

    # -----------------------------------------------------
    # VALIDATE INPUTS
    # -----------------------------------------------------

    all_inputs_filled = all([
        food_type is not None,
        number_of_guests is not None,
        event_type is not None,
        quantity_of_food is not None,
        storage_conditions is not None,
        purchase_history is not None,
        seasonality is not None,
        preparation_method is not None,
        geographical_location is not None,
        pricing is not None
    ])

    if not all_inputs_filled:

        st.warning(
            "⚠️ Please complete all the fields in the sidebar "
            "before predicting food waste."
        )

    else:

        # -------------------------------------------------
        # CREATE MODEL INPUT
        # Keep the original model feature names and order.
        # -------------------------------------------------

        input_data = pd.DataFrame({
            "Type of Food": [food_type],
            "Number of Guests": [number_of_guests],
            "Event Type": [event_type],
            "Quantity of Food": [quantity_of_food],
            "Storage Conditions": [storage_conditions],
            "Purchase History": [purchase_history],
            "Seasonality": [seasonality],
            "Preparation Method": [preparation_method],
            "Geographical Location": [geographical_location],
            "Pricing": [pricing]
        })

        try:

            # ---------------------------------------------
            # PREDICT FOOD WASTE
            # ---------------------------------------------

            prediction = float(model.predict(input_data)[0])

            if not pd.notna(prediction):
                raise ValueError(
                    "The model returned an invalid prediction."
                )

            prediction = max(0.0, prediction)

            # ---------------------------------------------
            # WASTE CALCULATIONS
            # ---------------------------------------------

            waste_percentage = (
                prediction / quantity_of_food
            ) * 100

            estimated_usable_quantity = max(
                0.0,
                quantity_of_food - prediction
            )

            # ---------------------------------------------
            # RISK CLASSIFICATION
            # ---------------------------------------------

            if waste_percentage < 20:
                waste_status = "Low"
                risk = "🟢 LOW WASTE RISK"
                risk_class = "risk-low"

                message = (
                    "The predicted waste is relatively low "
                    "compared with the prepared quantity. "
                    "Continue monitoring actual food demand."
                )

            elif waste_percentage < 40:
                waste_status = "Moderate"
                risk = "🟡 MODERATE WASTE RISK"
                risk_class = "risk-moderate"

                message = (
                    "Moderate waste is predicted. Review "
                    "guest demand and consider adjusting "
                    "the amount of food prepared."
                )

            else:
                waste_status = "High"
                risk = "🔴 HIGH WASTE RISK"
                risk_class = "risk-high"

                message = (
                    "A high proportion of food waste is "
                    "predicted. Review purchasing patterns "
                    "and preparation quantities."
                )

            # ---------------------------------------------
            # RECOMMENDED PREPARATION
            # Heuristic recommendation, not an ML output.
            # ---------------------------------------------

            if waste_percentage >= 40:
                reduction_rate = 0.10
                recommendation_reason = (
                    "A 10% reduction is suggested as a "
                    "starting point for reviewing food "
                    "preparation. Validate against actual demand."
                )

            elif waste_percentage >= 20:
                reduction_rate = 0.05
                recommendation_reason = (
                    "A 5% reduction is suggested as a "
                    "starting point. Review actual demand "
                    "before changing preparation quantities."
                )

            else:
                reduction_rate = 0.0
                recommendation_reason = (
                    "No reduction is suggested by this "
                    "simple rule. Continue monitoring actual "
                    "waste and guest demand."
                )

            recommended_quantity = (
                quantity_of_food * (1 - reduction_rate)
            )

            quantity_reduction = (
                quantity_of_food - recommended_quantity
            )

            # ---------------------------------------------
            # PROJECTED WASTE
            # ---------------------------------------------

            recommended_input = input_data.copy()

            recommended_input["Quantity of Food"] = (
                recommended_quantity
            )

            projected_waste = float(
                model.predict(recommended_input)[0]
            )

            if not pd.notna(projected_waste):
                raise ValueError(
                    "The model returned an invalid projected prediction."
                )

            projected_waste = max(
                0.0,
                min(projected_waste, recommended_quantity)
            )

            projected_waste_change = (
                prediction - projected_waste
            )

        except Exception as e:

            st.error("Unable to generate the prediction.")
            st.code(str(e))
            st.stop()

            
        # =================================================
        # SAVE PREDICTION HISTORY
        # =================================================

        history_path = Path("data/prediction_history.csv")

        history_record = {
            "Prediction Date": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "Food Type": food_type,
            "Quantity Prepared": quantity_of_food,
            "Number of Guests": number_of_guests,
            "Event Type": event_type,
            "Predicted Waste": round(prediction, 2),
            "Waste Percentage": round(waste_percentage, 2),
            "Recommended Quantity": round(
                recommended_quantity, 2
            ),
            "Risk Level": waste_status
        }

        try:
            history_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            history_df = pd.DataFrame([history_record])

            if (
                history_path.exists()
                and history_path.stat().st_size > 0
            ):
                history_df.to_csv(
                    history_path,
                    mode="a",
                    header=False,
                    index=False
                )
            else:
                history_df.to_csv(
                    history_path,
                    index=False
                )

        except Exception as e:
            st.warning(
                "Prediction completed, but history could "
                f"not be saved: {e}"
            )


        # =================================================
        # USER INPUT OVERVIEW
        # =================================================

        st.markdown(
            '<div class="section-title">📋 User Input Overview</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Review the values used by the prediction model."
        )

        input_col1, input_col2, input_col3, input_col4 = (
            st.columns(4)
        )

        with input_col1:
            input_card("Food Type", food_type)
            input_card("Food Quantity", f"{quantity_of_food} units")
            input_card("Preparation", preparation_method)

        with input_col2:
            input_card("Number of Guests", number_of_guests)
            input_card("Event Type", event_type)
            input_card("Season", seasonality)

        with input_col3:
            input_card("Storage Conditions", storage_conditions)
            input_card("Purchase History", purchase_history)
            input_card("Location", geographical_location)

        with input_col4:
            input_card("Pricing", pricing)

        # =================================================
        # WASTE ANALYSIS METRIC CARDS
        # =================================================

        st.markdown(
            '<div class="section-title">📊 Waste Analysis</div>',
            unsafe_allow_html=True
        )

        analysis_col1, analysis_col2, analysis_col3, analysis_col4 = (
            st.columns(4)
        )

        with analysis_col1:
            metric_card(
                "Predicted Waste",
                f"{prediction:.2f} units",
                "Estimated by the trained model"
            )

        with analysis_col2:
            metric_card(
                "Waste Percentage",
                f"{waste_percentage:.1f}%",
                "Relative to prepared quantity"
            )

        with analysis_col3:
            metric_card(
                "Prepared Quantity",
                f"{quantity_of_food} units",
                "User-provided quantity"
            )

        with analysis_col4:
            metric_card(
                "Estimated Remaining",
                f"{estimated_usable_quantity:.2f} units",
                "Prepared quantity minus predicted waste"
            )

        st.caption(
            f"Estimated waste risk: {waste_status}. "
            "Risk categories use simple percentage thresholds "
            "and are not independently calibrated risk probabilities."
        )

        # =================================================
        # PREDICTION RESULT
        # =================================================

        st.markdown(
            '<div class="section-title">🎯 Prediction Result</div>',
            unsafe_allow_html=True
        )

        result_col1, result_col2 = st.columns([1, 1])

        with result_col1:

            st.markdown(
                f"""
                <div class="result-box">
                    <div class="result-label">
                        PREDICTED FOOD WASTE
                    </div>
                    <div class="result-number">
                        {prediction:.2f}
                    </div>
                    <div class="result-unit">
                        Waste units
                    </div>
                    <br>
                    <div class="{risk_class}">
                        {risk}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with result_col2:

            st.markdown(
                f"""
                <div class="recommendation-box">
                    <div class="recommendation-title">
                        💡 Smart Recommendation
                    </div>
                    <div class="recommendation-text">
                        {html.escape(message)}
                        <br><br>
                        Predicted waste:
                        <b>{prediction:.2f} units</b>
                        <br>
                        Waste percentage:
                        <b>{waste_percentage:.1f}%</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # =================================================
        # RECOMMENDED PREPARATION
        # =================================================

        st.markdown(
            '<div class="section-title">🍽️ Recommended Preparation</div>',
            unsafe_allow_html=True
        )

        rec_col1, rec_col2, rec_col3 = st.columns(3)

        with rec_col1:
            metric_card(
                "Recommended Quantity",
                f"{recommended_quantity:.1f} units",
                "Rule-based suggested quantity"
            )

        with rec_col2:
            metric_card(
                "Suggested Reduction",
                f"{quantity_reduction:.1f} units",
                "Difference from planned quantity"
            )

        with rec_col3:
            metric_card(
                "Current Planned",
                f"{quantity_of_food} units",
                "Original user input"
            )

        st.info("💡 " + recommendation_reason)

        # =================================================
        # WASTE REDUCTION IMPACT
        # =================================================

        st.markdown(
            '<div class="section-title">📉 Waste Reduction Impact</div>',
            unsafe_allow_html=True
        )

        impact_col1, impact_col2, impact_col3 = st.columns(3)

        with impact_col1:
            metric_card(
                "Current Predicted Waste",
                f"{prediction:.2f} units",
                "Prediction using original quantity"
            )

        with impact_col2:
            metric_card(
                "Projected Waste",
                f"{projected_waste:.2f} units",
                "Prediction using suggested quantity"
            )

        with impact_col3:
            metric_card(
                "Predicted Waste Change",
                f"{projected_waste_change:+.2f} units",
                "Current prediction minus projected prediction"
            )

        st.caption(
            "Projected waste is a model estimate for the "
            "suggested quantity, not a guarantee of actual "
            "waste reduction. Validate recommendations using "
            "real-world observations."
        )

        st.success(
            "Prediction completed successfully. "
            "You can change the inputs in the sidebar and "
            "submit the form again."
        )

else:

    # =====================================================
    # INITIAL DASHBOARD / INPUT-ONLY OVERVIEW
    # =====================================================

    st.markdown(
        '<div class="section-title">👋 Welcome to FoodWise</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Use the sidebar to enter food and event details. "
        "Your input overview, metric cards, prediction result "
        "and recommendations will appear after you submit "
        "the prediction form."
    )

    welcome_col1, welcome_col2, welcome_col3 = st.columns(3)

    with welcome_col1:
        metric_card(
            "Machine Learning",
            "Random Forest",
            "Existing trained model"
        )

    with welcome_col2:
        metric_card(
            "Input Features",
            "10",
            "Food, event, storage and business details"
        )

    with welcome_col3:
        metric_card(
            "Prediction",
            "Ready",
            "Complete the sidebar form to begin"
        )

    st.info(
        "Select all required fields in the sidebar and click "
        "'Predict Food Waste' to view your personalized results."
    )




# =========================================================
# PREDICTION HISTORY
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">📜 Prediction History</div>',
    unsafe_allow_html=True
)

history_path = Path("data/prediction_history.csv")

if history_path.exists() and history_path.stat().st_size > 0:
    try:
        history_df = pd.read_csv(history_path)

        if not history_df.empty:
            display_history = history_df.sort_values(
                "Prediction Date",
                ascending=False
            )

            st.caption(
                f"Total predictions saved: {len(history_df)}"
            )

            st.dataframe(
                display_history,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                label="⬇️ Download Prediction History",
                data=history_df.to_csv(index=False).encode("utf-8"),
                file_name="prediction_history.csv",
                mime="text/csv"
            )
        else:
            st.info(
                "No prediction history available yet. "
                "Make your first prediction to get started."
            )

    except Exception as e:
        st.warning(
            f"Could not read prediction history: {e}"
        )
else:
    st.info(
        "No prediction history available yet. "
        "Make your first prediction to get started."
    )


    
# =========================================================
# INTERACTIVE ANALYTICS DASHBOARD
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">📊 Prediction Analytics Dashboard</div>',
    unsafe_allow_html=True
)

analytics_path = Path("data/prediction_history.csv")

if analytics_path.exists() and analytics_path.stat().st_size > 0:

    try:
        analytics_df = pd.read_csv(analytics_path)

        if not analytics_df.empty:

            # Convert values to suitable data types
            analytics_df["Predicted Waste"] = pd.to_numeric(
                analytics_df["Predicted Waste"],
                errors="coerce"
            )

            analytics_df["Waste Percentage"] = pd.to_numeric(
                analytics_df["Waste Percentage"],
                errors="coerce"
            )

            analytics_df["Prediction Date"] = pd.to_datetime(
                analytics_df["Prediction Date"],
                errors="coerce"
            )

            analytics_df = analytics_df.dropna(
                subset=[
                    "Predicted Waste",
                    "Waste Percentage",
                    "Prediction Date"
                ]
            )

            if not analytics_df.empty:

                # -----------------------------------------
                # SUMMARY METRICS
                # -----------------------------------------

                total_predictions = len(analytics_df)

                average_waste = analytics_df[
                    "Predicted Waste"
                ].mean()

                average_percentage = analytics_df[
                    "Waste Percentage"
                ].mean()

                highest_waste = analytics_df[
                    "Predicted Waste"
                ].max()

                metric_col1, metric_col2, metric_col3, metric_col4 = (
                    st.columns(4)
                )

                with metric_col1:
                    metric_card(
                        "Total Predictions",
                        total_predictions,
                        "Saved prediction records"
                    )

                with metric_col2:
                    metric_card(
                        "Average Predicted Waste",
                        f"{average_waste:.2f}",
                        "Waste units per prediction"
                    )

                with metric_col3:
                    metric_card(
                        "Average Waste Percentage",
                        f"{average_percentage:.1f}%",
                        "Average of recorded predictions"
                    )

                with metric_col4:
                    metric_card(
                        "Highest Predicted Waste",
                        f"{highest_waste:.2f}",
                        "Waste units in one prediction"
                    )

                st.divider()

                # -----------------------------------------
                # FILTERS
                # -----------------------------------------

                st.markdown(
    '<p style="font-size:20px; font-weight:650; color:#19385a; margin-bottom:8px;">'
    '🔎 Filter Analytics</p>',
    unsafe_allow_html=True
)

                filter_col1, filter_col2 = st.columns(2)

                with filter_col1:
                    food_options = [
                        "All Food Types"
                    ] + sorted(
                        analytics_df["Food Type"]
                        .dropna()
                        .astype(str)
                        .unique()
                        .tolist()
                    )

                    selected_food = st.selectbox(
                        "Select Food Type",
                        food_options,
                        key="analytics_food_filter"
                    )

                with filter_col2:
                    event_options = [
                        "All Events"
                    ] + sorted(
                        analytics_df["Event Type"]
                        .dropna()
                        .astype(str)
                        .unique()
                        .tolist()
                    )

                    selected_event = st.selectbox(
                        "Select Event Type",
                        event_options,
                        key="analytics_event_filter"
                    )

                filtered_df = analytics_df.copy()

                if selected_food != "All Food Types":
                    filtered_df = filtered_df[
                        filtered_df["Food Type"].astype(str)
                        == selected_food
                    ]

                if selected_event != "All Events":
                    filtered_df = filtered_df[
                        filtered_df["Event Type"].astype(str)
                        == selected_event
                    ]

                if filtered_df.empty:
                    st.info(
                        "No prediction records match the selected filters."
                    )

                else:
                    # -------------------------------------
                    # CHART 1: WASTE BY FOOD TYPE
                    # -------------------------------------

                    st.markdown(
    '<p style="font-size:20px; font-weight:650; color:#19385a; margin-bottom:8px;">'
    '🍎 Predicted Waste by Food Type</p>',
    unsafe_allow_html=True
)

                    waste_by_food = (
                        filtered_df.groupby("Food Type")[
                            "Predicted Waste"
                        ]
                        .mean()
                        .sort_values(ascending=False)
                    )

                    st.bar_chart(
                        waste_by_food,
                        x_label="Food Type",
                        y_label="Average Predicted Waste"
                    )

                    # -------------------------------------
                    # CHART 2: PREDICTIONS OVER TIME
                    # -------------------------------------

                    st.markdown(
    '<p style="font-size:20px; font-weight:650; color:#19385a; margin-bottom:8px;">'
    '📅 Prediction Trends</p>',
    unsafe_allow_html=True
)

                    daily_trends = (
                        filtered_df.assign(
                            PredictionDay=filtered_df[
                                "Prediction Date"
                            ].dt.date
                        )
                        .groupby("PredictionDay")[
                            "Predicted Waste"
                        ]
                        .mean()
                    )

                    st.line_chart(
                        daily_trends,
                        x_label="Prediction Date",
                        y_label="Average Predicted Waste"
                    )

                    # -------------------------------------
                    # CHART 3: WASTE PERCENTAGE
                    # -------------------------------------

                    st.markdown(
    '<p style="font-size:20px; font-weight:650; color:#19385a; margin-bottom:8px;">'
    '📈 Waste Percentage by Prediction</p>',
    unsafe_allow_html=True
)

                    percentage_chart = filtered_df[
                        ["Prediction Date", "Waste Percentage"]
                    ].copy()

                    percentage_chart = percentage_chart.sort_values(
                        "Prediction Date"
                    )

                    percentage_chart["Prediction"] = range(
                        1, len(percentage_chart) + 1
                    )

                    st.line_chart(
                        percentage_chart.set_index("Prediction")[
                            ["Waste Percentage"]
                        ],
                        x_label="Prediction Number",
                        y_label="Waste Percentage (%)"
                    )

                    # -------------------------------------
                    # HIGHEST AVERAGE WASTE
                    # -------------------------------------

                    st.markdown(
    '<p style="font-size:20px; font-weight:650; color:#19385a; margin-bottom:8px;">'
    '🏆 Food Waste Insights</p>',
    unsafe_allow_html=True
)

                    if not waste_by_food.empty:
                        highest_food = waste_by_food.index[0]
                        highest_food_value = waste_by_food.iloc[0]

                        st.info(
                            f"Among the filtered prediction records, "
                            f"**{highest_food}** has the highest average "
                            f"predicted waste: "
                            f"**{highest_food_value:.2f} units**."
                        )

                    st.caption(
                        "These charts summarize saved model predictions, "
                        "not verified measurements of actual food waste. "
                        "Results depend on the prediction history available."
                    )

            else:
                st.info(
                    "No valid prediction records are available for analytics."
                )

        else:
            st.info(
                "Make some predictions to populate the analytics dashboard."
            )

    except Exception as e:
        st.warning(
            f"Unable to load analytics: {e}"
        )

else:
    st.info(
        "Your analytics dashboard will appear after you save your first prediction."
    )







# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown("""
<div class="footer">
    🍽️ Food Waste Prediction System
    &nbsp; | &nbsp;
    Random Forest Regressor
    &nbsp; | &nbsp;
    Python + Streamlit
</div>
""", unsafe_allow_html=True)
