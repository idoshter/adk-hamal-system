# app.py

import pandas as pd
import streamlit as st

# עיצוב RTL
st.set_page_config(layout="wide")

def load_data():
    try:
        df = pd.read_csv("events_log.csv")
        return df
    except Exception as e:
        st.error(f"שגיאה בטעינת הקובץ: {e}")
        return pd.DataFrame()

st.markdown(
    """
    <style>
    body {
        direction: rtl;
        text-align: right;
        font-family: 'Arial';
    }
    .css-18e3th9 {
        direction: rtl;
    }
    .stDataFrame {
        direction: rtl;
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📋 מערכת צפייה באירועים")

df = load_data()

if df.empty:
    st.warning("לא נמצאו נתונים בקובץ.")
else:
    # סינון לפי סוג אירוע
    event_types = df["event_type"].dropna().unique()
    selected_types = st.multiselect("סוגי אירועים לסינון:", event_types, default=list(event_types))

    filtered_df = df[df["event_type"].isin(selected_types)]

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )
