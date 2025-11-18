import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# -----------------------------
# CONFIG – UPDATE COLUMN NAMES HERE
# -----------------------------
BUG_ID_COL = "Bug_ID"
MODULE_COL = "Module_Category"
STATUS_COL = "Status"
PRIORITY_COL = "Priority"
SEVERITY_COL = "Severity"
ASSIGNEE_COL = "Assignee"
CREATED_DATE_COL = "Created_Date"
CLOSED_DATE_COL = "Closed_Date"
CUSTOMER_COL = "Customer"
ENV_COL = "Environment"
RELEASE_COL = "Release"

OPEN_STATUS_VALUES = ["Open", "In Progress", "Reopened", "Assigned"]
CLOSED_STATUS_VALUES = ["Closed", "Resolved", "Verified"]

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Bug Rescue Operations Dashboard",
    layout="wide",
)

st.title("🐞 Bug Rescue Operations Dashboard")
st.caption(
    "Monitor total bugs and focus on high-risk areas by module, status, and priority."
)

# -----------------------------
# SIDEBAR – FILE + FILTERS
# -----------------------------
with st.sidebar:
    st.header("📂 Data Source")
    uploaded_file = st.file_uploader(
        "Upload bug dump (Excel)", type=["xlsx", "xls"]
    )

    st.markdown("---")
    st.subheader("🔎 Global Filters")

# Helper to safely read Excel
@st.cache_data
def load_data(file):
    return pd.read_excel(file)

def parse_date_safe(series):
    try:
        return pd.to_datetime(series, errors="coerce")
    except Exception:
        return pd.to_datetime(pd.Series([], dtype="datetime64[ns]"))

# -----------------------------
# MAIN LOGIC
# -----------------------------
if uploaded_file is None:
    st.info("⬆️ Please upload your `V6Bugs_All Modules.xlsx` (or similar) to see the dashboard.")
    st.stop()

# Load data
df = load_data(uploaded_file)

# Ensure required columns exist
required_cols = [MODULE_COL, STATUS_COL, PRIORITY_COL]
missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f"Missing required columns in file: {', '.join(missing)}")
    st.stop()

# Optional columns
for col_name in [
    BUG_ID_COL,
    SEVERITY_COL,
    ASSIGNEE_COL,
    CREATED_DATE_COL,
    CLOSED_DATE_COL,
    CUSTOMER_COL,
    ENV_COL,
    RELEASE_COL,
]:
    if col_name not in df.columns:
        # Create empty column if missing, to avoid errors.
        df[col_name] = None

# Date parsing + bug age
df[CREATED_DATE_COL] = parse_date_safe(df[CREATED_DATE_COL])
df[CLOSED_DATE_COL] = parse_date_safe(df[CLOSED_DATE_COL])

today = datetime.today().date()
df["Bug_Age_Days"] = (today - df[CREATED_DATE_COL].dt.date).dt.days

# -----------------------------
# SIDEBAR FILTERS (AFTER LOAD)
# -----------------------------
with st.sidebar:
    customer_filter = st.multiselect(
        "Customer", sorted([c for c in df[CUSTOMER_COL].dropna().unique()])
    )
    env_filter = st.multiselect(
        "Environment", sorted([c for c in df[ENV_COL].dropna().unique()])
    )
    release_filter = st.multiselect(
        "Release / Version", sorted([c for c in df[RELEASE_COL].dropna().unique()])
    )
    module_filter = st.multiselect(
        "Module Category", sorted([c for c in df[MODULE_COL].dropna().unique()])
    )
    priority_filter = st.multiselect(
        "Priority", sorted([c for c in df[PRIORITY_COL].dropna().unique()])
    )
    status_filter = st.multiselect(
        "Status", sorted([c for c in df[STATUS_COL].dropna().unique()])
    )

    st.markdown("---")
    st.caption("Tip: Use filters to focus on one customer, environment, or release.")


# Apply filters
filtered_df = df.copy()

if customer_filter:
    filtered_df = filtered_df[filtered_df[CUSTOMER_COL].isin(customer_filter)]

if env_filter:
    filtered_df = filtered_df[filtered_df[ENV_COL].isin(env_filter)]

if release_filter:
    filtered_df = filtered_df[filtered_df[RELEASE_COL].isin(release_filter)]

if module_filter:
    filtered_df = filtered_df[filtered_df[MODULE_COL].isin(module_filter)]

if priority_filter:
    filtered_df = filtered_df[filtered_df[PRIORITY_COL].isin(priority_filter)]

if status_filter:
    filtered_df = filtered_df[filtered_df[STATUS_COL].isin(status_filter)]

# -----------------------------
# KPI CARDS
# -----------------------------
total_bugs = len(filtered_df)
open_bugs = filtered_df[filtered_df[STATUS_COL].isin(OPEN_STATUS_VALUES)]
closed_bugs = filtered_df[filtered_df[STATUS_COL].isin(CLOSED_STATUS_VALUES)]

high_priority = filtered_df[filtered_df[PRIORITY_COL].isin(["P0", "P1", "Critical", "High"])]
old_open = open_bugs[open_bugs["Bug_Age_Days"] > 7]  # older than 7 days

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Bugs", f"{total_bugs}")
col2.metric("Open Bugs", f"{len(open_bugs)}")
col3.metric("Closed / Resolved", f"{len(closed_bugs)}")
col4.metric("High Priority (P0/P1/High)", f"{len(high_priority)}")

st.markdown("---")

# -----------------------------
# PIE CHARTS ROW – MODULE / STATUS / PRIORITY
# -----------------------------
col_a, col_b, col_c = st.columns(3)

# Pie – by Module Category
with col_a:
    st.subheader("By Module Category")
    module_counts = (
        filtered_df.groupby(MODULE_COL)[BUG_ID_COL if BUG_ID_COL in df.columns else STATUS_COL]
        .count()
        .reset_index()
        .rename(columns={BUG_ID_COL if BUG_ID_COL in df.columns else STATUS_COL: "Count"})
    )
    if not module_counts.empty:
        fig_mod = px.pie(
            module_counts,
            names=MODULE_COL,
            values="Count",
            hole=0.3,
        )
        fig_mod.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_mod, use_container_width=True)
    else:
        st.info("No data after filters for Module Category.")

# Pie – by Status
with col_b:
    st.subheader("By Status")
    status_counts = (
        filtered_df.groupby(STATUS_COL)[BUG_ID_COL if BUG_ID_COL in df.columns else PRIORITY_COL]
        .count()
        .reset_index()
        .rename(columns={BUG_ID_COL if BUG_ID_COL in df.columns else PRIORITY_COL: "Count"})
    )
    if not status_counts.empty:
        fig_status = px.pie(
            status_counts,
            names=STATUS_COL,
            values="Count",
            hole=0.3,
        )
        fig_status.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_status, use_container_width=True)
    else:
        st.info("No data after filters for Status.")

# Pie – by Priority
with col_c:
    st.subheader("By Priority")
    priority_counts = (
        filtered_df.groupby(PRIORITY_COL)[BUG_ID_COL if BUG_ID_COL in df.columns else STATUS_COL]
        .count()
        .reset_index()
        .rename(columns={BUG_ID_COL if BUG_ID_COL in df.columns else STATUS_COL: "Count"})
    )
    if not priority_counts.empty:
        fig_priority = px.pie(
            priority_counts,
            names=PRIORITY_COL,
            values="Count",
            hole=0.3,
        )
        fig_priority.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_priority, use_container_width=True)
    else:
        st.info("No data after filters for Priority.")

st.markdown("---")

# -----------------------------
# TABS – DEEP DIVE VIEWS
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["🔥 High-Risk View", "👨‍💻 By Assignee", "📈 Trend (Created vs Closed)", "📋 Raw Data"]
)

# 1️⃣ High-Risk View
with tab1:
    st.subheader("🔥 High-Risk Bugs (P0/P1/Critical/High)")
    risky = high_priority.sort_values("Bug_Age_Days", ascending=False)

    if risky.empty:
        st.info("No high-priority bugs for current filters.")
    else:
        st.write("Sorted by oldest open first:")
        st.dataframe(
            risky[
                [
                    BUG_ID_COL,
                    MODULE_COL,
                    STATUS_COL,
                    PRIORITY_COL,
                    SEVERITY_COL,
                    ASSIGNEE_COL,
                    CUSTOMER_COL,
                    ENV_COL,
                    RELEASE_COL,
                    CREATED_DATE_COL,
                    "Bug_Age_Days",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

        module_risk = (
            risky.groupby(MODULE_COL)[BUG_ID_COL if BUG_ID_COL in df.columns else STATUS_COL]
            .count()
            .reset_index()
            .rename(columns={BUG_ID_COL if BUG_ID_COL in df.columns else STATUS_COL: "High Risk Count"})
        )
        if not module_risk.empty:
            fig_risk = px.bar(
                module_risk,
                x=MODULE_COL,
                y="High Risk Count",
            )
            st.plotly_chart(fig_risk, use_container_width=True)

# 2️⃣ By Assignee
with tab2:
    st.subheader("👨‍💻 Open Bugs by Assignee")
    assignee_open = (
        open_bugs.groupby(ASSIGNEE_COL)[BUG_ID_COL if BUG_ID_COL in df.columns else STATUS_COL]
        .count()
        .reset_index()
        .rename(columns={BUG_ID_COL if BUG_ID_COL in df.columns else STATUS_COL: "Open Bugs"})
    )
    assignee_open = assignee_open.sort_values("Open Bugs", ascending=False)

    if not assignee_open.empty:
        fig_assignee = px.bar(
            assignee_open,
            x="Open Bugs",
            y=ASSIGNEE_COL,
            orientation="h",
        )
        st.plotly_chart(fig_assignee, use_container_width=True)
        st.dataframe(assignee_open, use_container_width=True, hide_index=True)
    else:
        st.info("No open bugs for current filters.")

# 3️⃣ Trend – Created vs Closed
with tab3:
    st.subheader("📈 Bugs Created vs Closed (per Day)")

    if filtered_df[CREATED_DATE_COL].notna().any():
        created = (
            filtered_df.dropna(subset=[CREATED_DATE_COL])
            .assign(Date=filtered_df[CREATED_DATE_COL].dt.date)
            .groupby("Date")[BUG_ID_COL if BUG_ID_COL in df.columns else STATUS_COL]
            .count()
            .reset_index()
            .rename(columns={BUG_ID_COL if BUG_ID_COL in df.columns else STATUS_COL: "Created"})
        )
    else:
        created = pd.DataFrame(columns=["Date", "Created"])

    if filtered_df[CLOSED_DATE_COL].notna().any():
        closed = (
            filtered_df.dropna(subset=[CLOSED_DATE_COL])
            .assign(Date=filtered_df[CLOSED_DATE_COL].dt.date)
            .groupby("Date")[BUG_ID_COL if BUG_ID_COL in df.columns else STATUS_COL]
            .count()
            .reset_index()
            .rename(columns={BUG_ID_COL if BUG_ID_COL in df.columns else STATUS_COL: "Closed"})
        )
    else:
        closed = pd.DataFrame(columns=["Date", "Closed"])

    trend = pd.merge(created, closed, on="Date", how="outer").fillna(0)
    if not trend.empty:
        fig_trend = px.line(
            trend.sort_values("Date"),
            x="Date",
            y=["Created", "Closed"],
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        st.dataframe(trend.sort_values("Date"), use_container_width=True, hide_index=True)
    else:
        st.info("No date information available for trend chart.")

# 4️⃣ Raw Data
with tab4:
    st.subheader("📋 Filtered Data")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    # Download button
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download filtered data as CSV",
        data=csv,
        file_name="bug_rescue_filtered_data.csv",
        mime="text/csv",
    )
