import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Configuration and Title ---
st.set_page_config(layout="wide")
st.title("Comprehensive Sleep Survey Analysis")
st.markdown("This application visualizes survey data using 8 interactive Plotly charts.")

#Visualization 1

# Count the age groups
age_counts = df['Your Age'].value_counts().reset_index()
age_counts.columns = ['Age Group', 'Count']

# Create the pie chart
fig = px.pie(
    age_counts,
    names='Age Group',
    values='Count',
    title='Distribution of Age Groups (Pastel Theme)',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# Make it look balanced (like plt.axis('equal'))
fig.update_traces(textposition='inside', textinfo='percent+label', rotation=140)
fig.update_layout(showlegend=True)

fig.show()
