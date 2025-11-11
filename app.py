
import pandas as pd
import streamlit as st

st.set_page_config(page_title="SplashBI — AutoML Configuration", layout="centered")

LOGO_PATH = "splashbi.png"

# ----------------------------
# Branding Header
# ----------------------------
header = st.container()
with header:
    cols = st.columns([0.2, 0.8])
    with cols[0]:
        try:
            st.image(LOGO_PATH, use_container_width=True)
        except Exception:
            st.write("SplashBI")
    with cols[1]:
        st.markdown("<h2 style='margin-bottom:0'>AutoML</h2>", unsafe_allow_html=True)
        st.caption("Build, train, deploy and manage machine learning models using AutoML")

st.markdown("---")

# ----------------------------
# Styles
# ----------------------------
st.markdown(
    """
    <style>
      .form-card{
        border:1px solid #e5e7eb;
        border-radius:16px;
        padding:20px 22px;
        background:#ffffff;
      }
      .stButton>button {
        border-radius:10px;
        padding:8px 16px;
      }
      .muted{color:#6b7280;font-size:0.9rem}
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Demo metadata
# ----------------------------
DEMO_TABLES = {
    "Churn_History_Data": [
        "Customer_ID","Tenure","Usage","Support_Tickets","Total_Transaction_Credits","Customer_Lifetime",
        "Marital_Status","Income_Category","Churn_Flag"
    ],
    "Employee_Attrition": [
        "Emp_ID","Tenure_Years","Salary","Performance_Score","Avg_Utilization_Ratio","Department","Attrition_Flag"
    ],
    "AR_Invoices": [
        "Invoice_ID","Amount","Days_Past_Due","Credit_Limit","Customer_Tier","Is_Paid"
    ]
}

CLASSIFIERS = [
    "Logistic Regression","Decision Tree Classification","Random Forest Classification",
    "Gradient Boosting Classification","XGBoost Classifier","SVM Classifier","Naive Bayes"
]
REGRESSORS = [
    "Linear Regression","Ridge Regression","Lasso Regression","Random Forest Regression",
    "Gradient Boosting Regression","XGBoost Regressor","SVR"
]

# ----------------------------
# Session defaults
# ----------------------------
ss = st.session_state
ss.setdefault("analysis_name", "New Analysis-1")
ss.setdefault("training_table", "Churn_History_Data")
ss.setdefault("prediction_type", "Classification")
ss.setdefault("df_from_csv", None)

# ----------------------------
# Helper to get available columns
# ----------------------------
def available_columns():
    if ss.get("df_from_csv") is not None:
        return list(ss["df_from_csv"].columns)
    return DEMO_TABLES.get(ss["training_table"], [])

# ----------------------------
# Main Form
# ----------------------------
st.markdown("<div class='form-card'>", unsafe_allow_html=True)

st.markdown("### Configuration")

# Analysis Name
ss.analysis_name = st.text_input("Analysis Name:", value=ss.analysis_name)

# Description
description = st.text_area("Description:", placeholder="Describe the objective of this analysis…", height=80)

# Training Source
st.markdown("##### Training Source")
source_mode = st.radio("Select Source", options=["Demo Table","Upload CSV"], horizontal=True, label_visibility="collapsed")

if source_mode == "Demo Table":
    ss.training_table = st.selectbox("Training Table:", options=list(DEMO_TABLES.keys()), index=list(DEMO_TABLES.keys()).index(ss.training_table))
    # If switching back from CSV, clear uploaded frame
    ss.df_from_csv = None
else:
    up = st.file_uploader("Upload CSV", type=["csv"])
    if up is not None:
        try:
            ss.df_from_csv = pd.read_csv(up)
            st.success(f"Loaded CSV: {ss.df_from_csv.shape[0]} rows × {ss.df_from_csv.shape[1]} columns")
            with st.expander("Preview (top 10 rows)", expanded=False):
                st.dataframe(ss.df_from_csv.head(10), use_container_width=True)
        except Exception as e:
            st.error(f"Could not read CSV: {e}")

# Target Column
cols = available_columns()
target_opts = cols if cols else ["—"]
target_col = st.selectbox("Target Column:", options=target_opts, index=target_opts.index("—") if "—" in target_opts else 0)

# Feature List (chips via multiselect)
st.markdown("##### Feature List")
feat_suggestion = [c for c in cols if c != target_col]
default_feats = [f for f in feat_suggestion[:2]]  # pick first two by default
features = st.multiselect("Choose Features:", options=feat_suggestion, default=default_feats, help="Hold Ctrl/Cmd to select multiple")

# Prediction Type
st.markdown("##### Prediction Type")
ss.prediction_type = st.selectbox("Prediction Type:", options=["Classification","Regression"], index=0 if ss.prediction_type=="Classification" else 1)

# Algorithm picker depends on prediction type
st.markdown("##### Algorithm")
algo_pool = CLASSIFIERS if ss.prediction_type == "Classification" else REGRESSORS
algorithms = st.multiselect("Add Algorithms:", options=algo_pool, default=algo_pool[:2])

st.markdown("---")
c1, c2, c3 = st.columns([1,1,2])
with c1:
    save_draft = st.button("Save As Draft")
with c2:
    create_train = st.button("Create & Train")

# ----------------------------
# Actions
# ----------------------------
if save_draft:
    st.info("Draft saved (in-memory). You can persist this to your backend in integration.")
if create_train:
    # Basic validations
    if target_col in (None, "", "—"):
        st.warning("Please select a valid Target Column.")
    elif not features:
        st.warning("Please select at least one Feature.")
    elif not algorithms:
        st.warning("Please choose at least one Algorithm.")
    else:
        st.success("Configuration complete. Training job initialized.")
        with st.expander("Summary", expanded=True):
            st.write({
                "Analysis Name": ss.analysis_name,
                "Description": (description or "").strip()[:200],
                "Source": ("CSV Upload" if ss.get("df_from_csv") is not None else f"Demo Table: {ss.training_table}"),
                "Target Column": target_col,
                "Features": features,
                "Prediction Type": ss.prediction_type,
                "Algorithms": algorithms
            })
        st.caption("→ Hook this event to your training service or AutoML backend.")

st.markdown("</div>", unsafe_allow_html=True)

st.caption("© SplashBI — AutoML Configuration (Left Panel Only)")
