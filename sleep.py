import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Configuration and Title ---
st.set_page_config(layout="wide")
st.title("Comprehensive Sleep Survey Analysis")
st.markdown("This application visualizes survey data using 8 interactive Plotly charts.")


# --- Dummy Data Creation (REPLACE with your actual df loading) ---
@st.cache_data
def load_data():
    # Define columns
    gender_col = 'What is your gender?'
    occupation_col = 'What is your occupation?'
    sleep_col = 'How many hours of sleep do you get on average per night?'
    age_col = 'Your Age'
    reasons_col = 'What are the main reasons you sleep late?'
    side_effects_col = 'Do you experience any of the following side effects from late sleeping?'
    difficulty_col = 'Do you have difficulty falling asleep?'
    concentrate_col = 'How often do you find it hard to concentrate due to lack of sleep?'
    comfort_col = 'How would you rate the comfort of your sleeping environment'
    
    # Create realistic dummy data (100 respondents)
    data = {
        age_col: np.random.choice(['18-24', '25-34', '35-44', '45-54', '55+'], 100, p=[0.25, 0.35, 0.20, 0.10, 0.10]),
        gender_col: np.random.choice(['Male', 'Female'], 100, p=[0.55, 0.45]),
        occupation_col: np.random.choice(['Student', 'Employed', 'Self-Employed', 'Unemployed'], 100, p=[0.25, 0.40, 0.25, 0.10]),
        sleep_col: np.random.choice(['< 5 hours', '5-6 hours', '6-7 hours', '7-8 hours', '> 8 hours'], 100, p=[0.1, 0.2, 0.3, 0.25, 0.15]),
        reasons_col: ['Social Media; Entertainment', 'Work Stress; Late Meals', 'Entertainment', 'Work Stress', 'Social Media'] * 20,
        side_effects_col: ['Fatigue; Irritability', 'Lack of Concentration', 'None', 'Fatigue'] * 25,
        difficulty_col: np.random.choice(['Yes', 'No'], 100, p=[0.4, 0.6]),
        concentrate_col: np.random.choice(['Never', 'Sometimes', 'Often', 'Always'], 100, p=[0.2, 0.4, 0.3, 0.1]),
        comfort_col: np.random.choice(['Very Low', 'Low', 'Moderate', 'High', 'Very High'], 100, p=[0.05, 0.15, 0.3, 0.35, 0.15]),
    }
    df = pd.DataFrame(data)
    
    return df, gender_col, occupation_col, sleep_col, age_col, reasons_col, side_effects_col, difficulty_col, concentrate_col, comfort_col

df, gender_col, occupation_col, sleep_col, age_col, reasons_col, side_effects_col, difficulty_col, concentrate_col, comfort_col = load_data()

# Custom colors defined in the original code
CUSTOM_PINK_BLUE_PALETTE = ["#ADD8E6", "#FFB6C1"] 
COLOR_MAP = {'Male': CUSTOM_PINK_BLUE_PALETTE[0], 'Female': CUSTOM_PINK_BLUE_PALETTE[1]}


# --- 1. Occupation Distribution Grouped by Gender (Grouped Bar Chart) ---
st.header("1. Occupation Distribution by Gender")
count_df_1 = df.groupby([occupation_col, gender_col]).size().reset_index(name='Count')
occupation_order_1 = df[occupation_col].value_counts().index.tolist()

fig1 = px.bar(
    count_df_1, x=occupation_col, y='Count', color=gender_col,
    barmode='group', title='Occupation Distribution Grouped by Gender',
    category_orders={occupation_col: occupation_order_1},
    color_discrete_map=COLOR_MAP
)
fig1.update_layout(xaxis_title=occupation_col, yaxis_title='Number of Respondents (Count)', xaxis_tickangle=-30)
st.plotly_chart(fig1, use_container_width=True)

# --- 2. Sleep Duration by Gender (Normalized Stacked Bar Chart) ---
st.header("2. Sleep Duration by Gender (Normalized)")
ct_2 = pd.crosstab(df[gender_col], df[sleep_col])
ct_normalized_2 = ct_2.div(ct_2.sum(axis=1), axis=0) * 100
ct_normalized_2 = ct_normalized_2.reset_index().melt(
    id_vars=gender_col, var_name=sleep_col, value_name='Proportion (%)'
)

# Ensure consistent order for sleep categories
sleep_order_2 = ['< 5 hours', '5-6 hours', '6-7 hours', '7-8 hours', '> 8 hours']
ct_normalized_2[sleep_col] = pd.Categorical(ct_normalized_2[sleep_col], categories=sleep_order_2, ordered=True)
ct_normalized_2 = ct_normalized_2.sort_values(sleep_col)

fig2 = px.bar(
    ct_normalized_2, x=gender_col, y='Proportion (%)', color=sleep_col,
    title='Proportion of Sleep Duration by Gender',
    color_discrete_sequence=px.colors.sequential.Viridis,
)
fig2.update_layout(yaxis_title='Proportion (%)', xaxis_title=gender_col)
st.plotly_chart(fig2, use_container_width=True)

# --- 3. Difficulty Falling Asleep by Gender (Grouped Bar Chart) ---
st.header("3. Difficulty Falling Asleep by Gender")
count_df_3 = df.groupby([difficulty_col, gender_col]).size().reset_index(name='Count')

fig3 = px.bar(
    count_df_3, x=difficulty_col, y='Count', color=gender_col,
    barmode='group', title='Difficulty Falling Asleep by Gender',
    color_discrete_map=COLOR_MAP
)
fig3.update_layout(xaxis_title=difficulty_col, yaxis_title='Count', xaxis_tickangle=-30)
st.plotly_chart(fig3, use_container_width=True)

# --- 4. Difficulty Falling Asleep vs. Concentration (Heatmap) ---
st.header("4. Difficulty Falling Asleep vs. Difficulty Concentrating (Heatmap)")
contingency_table_4 = pd.crosstab(df[difficulty_col], df[concentrate_col])

fig4 = px.imshow(
    contingency_table_4.values,
    x=contingency_table_4.columns,
    y=contingency_table_4.index,
    color_continuous_scale='BuPu',  # Equivalent to soft_bupu_cmap
    labels={'x': concentrate_col, 'y': difficulty_col, 'color': 'Count'},
    text_auto=True  # Adds annotations (fmt='d')
)
fig4.update_layout(title='Relationship between Difficulty Falling Asleep and Difficulty Concentrating')
fig4.update_xaxes(tickangle=45)
st.plotly_chart(fig4, use_container_width=True)

# --- 5. Reasons for Sleeping Late by Age Group (Normalized Stacked Bar) ---
st.header("5. Reasons for Sleeping Late by Age Group (Normalized)")
reasons_df_5 = df[[age_col, reasons_col]].copy()
reasons_df_5[reasons_col] = reasons_df_5[reasons_col].str.split(';')
reasons_df_5 = reasons_df_5.explode(reasons_col).dropna()
reasons_df_5[reasons_col] = reasons_df_5[reasons_col].str.strip()

# Create normalized table for plotting
ct_5 = pd.crosstab(reasons_df_5[age_col], reasons_df_5[reasons_col])
ct_normalized_5 = ct_5.div(ct_5.sum(axis=1), axis=0) * 100
ct_normalized_5 = ct_normalized_5.reset_index().melt(
    id_vars=age_col, var_name=reasons_col, value_name='Proportion (%)'
)

age_order_5 = ['18-24', '25-34', '35-44', '45-54', '55+']
ct_normalized_5[age_col] = pd.Categorical(ct_normalized_5[age_col], categories=age_order_5, ordered=True)
ct_normalized_5 = ct_normalized_5.sort_values(age_col)

fig5 = px.bar(
    ct_normalized_5, x=age_col, y='Proportion (%)', color=reasons_col,
    title='Reasons for Sleeping Late by Age Group (Normalized)',
    color_discrete_sequence=px.colors.sequential.Viridis
)
fig5.update_layout(xaxis_title='Age Group', yaxis_title='Proportion (%)', xaxis_tickangle=-45)
st.plotly_chart(fig5, use_container_width=True)

# --- 6. Comfort vs. Sleep Hours (Line Plot / Multi-series Scatter) ---
st.header("6. Comfort vs. Sleep Hours (Multi-series Scatter)")
grouped_comfort_6 = df.groupby([sleep_col, comfort_col]).size().unstack(fill_value=0)
grouped_comfort_6 = grouped_comfort_6.reset_index().melt(
    id_vars=sleep_col, var_name=comfort_col, value_name='Count'
)

# Order categories
sleep_order_6 = ['< 5 hours', '5-6 hours', '6-7 hours', '7-8 hours', '> 8 hours']
comfort_order_6 = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']
grouped_comfort_6[sleep_col] = pd.Categorical(grouped_comfort_6[sleep_col], categories=sleep_order_6, ordered=True)
grouped_comfort_6[comfort_col] = pd.Categorical(grouped_comfort_6[comfort_col], categories=comfort_order_6, ordered=True)
grouped_comfort_6 = grouped_comfort_6.sort_values([sleep_col, comfort_col])

fig6 = px.line(
    grouped_comfort_6, x=comfort_col, y='Count', color=sleep_col,
    title='Comfort of Sleeping Environment Ratings by Average Hours of Sleep per Night',
    markers=True,
    category_orders={comfort_col: comfort_order_6, sleep_col: sleep_order_6},
    color_discrete_sequence=px.colors.sequential.Viridis
)
fig6.update_layout(xaxis_title='Rating', yaxis_title='Count')
st.plotly_chart(fig6, use_container_width=True)

# --- 7. Average Sleep Hours vs. Side Effects (Heatmap) ---
st.header("7. Average Sleep Hours vs. Side Effects (Heatmap)")
side_effects_df_7 = df[[sleep_col, side_effects_col]].copy()
side_effects_df_7[side_effects_col] = side_effects_df_7[side_effects_col].str.split(';')
side_effects_df_7 = side_effects_df_7.explode(side_effects_col).dropna()
side_effects_df_7[side_effects_col] = side_effects_df_7[side_effects_col].str.strip()

contingency_table_7 = pd.crosstab(side_effects_df_7[sleep_col], side_effects_df_7[side_effects_col])

fig7 = px.imshow(
    contingency_table_7.values,
    x=contingency_table_7.columns,
    y=contingency_table_7.index,
    color_continuous_scale='BuPu', 
    labels={'x': side_effects_col, 'y': sleep_col, 'color': 'Count'},
    text_auto=True
)
fig7.update_layout(title='Relationship between Average Sleep Hours and Side Effects')
fig7.update_xaxes(tickangle=45)
st.plotly_chart(fig7, use_container_width=True)

# --- 8. Comfort Rating by Difficulty Concentrating (Facet Bar Chart) ---
st.header("8. Comfort Rating by Difficulty Concentrating (Faceted Bar)")
count_df_8 = df.groupby([comfort_col, concentrate_col]).size().reset_index(name='Count')

# Order categories
concentration_order_8 = ['Never', 'Sometimes', 'Often', 'Always']
comfort_order_8 = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']
count_df_8[concentrate_col] = pd.Categorical(count_df_8[concentrate_col], categories=concentration_order_8, ordered=True)
count_df_8[comfort_col] = pd.Categorical(count_df_8[comfort_col], categories=comfort_order_8, ordered=True)
count_df_8 = count_df_8.sort_values([concentrate_col, comfort_col])

fig8 = px.bar(
    count_df_8, 
    x=comfort_col, 
    y='Count', 
    facet_col=concentrate_col, 
    facet_col_wrap=4,
    title='Comfort of Sleeping Environment Ratings by Difficulty Concentrating',
    # Use a single gradient color for better contrast against the facet background
    color_discrete_sequence=px.colors.sequential.Sunsetdark 
)
fig8.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1])) # Clean up facet titles
fig8.update_layout(xaxis_title="Comfort Rating", yaxis_title="Count")
fig8.update_xaxes(tickangle=45)
st.plotly_chart(fig8, use_container_width=True)
