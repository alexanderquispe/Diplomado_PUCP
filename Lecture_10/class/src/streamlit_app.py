import streamlit as st
from estimation import execute_regressions, generate_data
from plots import *

data = generate_data()
results, results_data = execute_regressions(data)

st.set_page_config(page_title="Simpson's Paradox", layout="wide")

tab1, tab2, tab3 = st.tabs(["Simpson's Paradox", "Code", "References"])

with tab1:

        st.markdown(
"""
# Simpson's Paradox Explained

Simpson's paradox posits that, when we calculate correlations in aggregated data for a given population, we may fin a positive (negative) correlation, but when the data are disaggregated, the correlation may have the opposite sign.

In this case, we simulate data such that we have a confounding variable, namely age. If age has an effect both exercise and cholesterol, not taking it into account when performing our estimation will will render us a biased estimator of the correlation between cholesterol and exercise. In this case, the bias is large enough that it reverts the sign: our correlation initially is positive, but when we segregate by age, the correlation is negative.

The data generating process is illustrated by the DAG further down bellow.
"""
        )
        col1, col2 = st.columns([1, 2])
        st.write("---")

        with col1:
                st.markdown("### Options")
                segregated = st.checkbox(label="Segregate by age")
                fit_line = st.checkbox(label="Show regression line", value=True)
                st.write("---")
                

        fig = get_figure(results_data, segregated, fit_line, )
        table = get_table(results, segregated)

        with col1:
                st.markdown("### Regression Results")
                st.table(table)



        with col2:
                st.markdown("### Scatter Plot")
                st.plotly_chart(fig, use_container_width=True)
                st.write("---")
                st.markdown("### DAG")
                if segregated:
                        st.image("assets/segregated.png")
                else:
                        st.image("assets/aggregated.png")

with tab2:
        st.markdown("""
### Code

Our code is hosted in the following GithHub repository: https://github.com/RodrigoGrijalba/python-dashboard-class
"""
)

with tab3:
        st.markdown("""
### References:

Glymour, Madelyn, Judea Pearl, and Nicholas P. Jewell. Causal inference in statistics: A primer. John Wiley & Sons, 2016. 
"""
)



