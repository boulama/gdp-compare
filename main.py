import streamlit as st
import pandas as pd
import altair as alt



file_path = "gdp.xls"
df = pd.read_excel(file_path, sheet_name="Data", skiprows=3)
df = df.drop(['Country Code', 'Indicator Code', 'Indicator Name'], axis=1)

st.title("GDP Data Explorer")
selected_countries = st.multiselect("Select Countries", df[df.columns[0]].unique(), default=['Niger', 'Cote d\'Ivoire'])

if selected_countries:
    st.write("### GDP Data for Selected Countries")
    countries_data = df[df[df.columns[0]].isin(selected_countries)]

    melted_data = pd.melt(countries_data, id_vars=[df.columns[0]], var_name="Year", value_name="GDP")

    pivoted_data = melted_data.pivot(index='Year', columns=df.columns[0], values='GDP')

    with st.container():
        chart = alt.Chart(melted_data).mark_line().encode(
            x='Year:T',
            y='GDP:Q',
            color=df.columns[0]
        ).properties(width=800, height=400)

        st.altair_chart(chart, theme='streamlit')
        st.write("Note: The color represents the selected country names.")

        st.write(pivoted_data.style.format("${:,.2f}"))