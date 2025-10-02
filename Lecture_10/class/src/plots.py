import plotly.graph_objects as go
import pandas as pd

def get_figure(plot_data, segregated, fit_line):
        fig = go.Figure(layout = go.Layout(width=900))
        fig.update_xaxes(title_text = "Exercise")
        fig.update_yaxes(title_text = "Cholesterol")
        if not segregated:
                fig.add_trace(go.Scatter(
                        x = plot_data.exercise,
                        y = plot_data.cholesterol,
                        mode = "markers",
                        showlegend = False,
                        marker_color = "black"
                ))
                if fit_line:
                        fig.add_trace(go.Scatter(
                                x = plot_data.exercise,
                                y = plot_data.aggregated_fit,
                                showlegend = False,
                                marker_color = "red"
                        ))
                        return fig
                return fig
        for age, group in plot_data.groupby("age_groups"):
                fig.add_trace(go.Scatter(
                        x = group.exercise,
                        y = group.cholesterol,
                        mode = "markers",
                        name = age
                ))
                if fit_line:
                        fig.add_trace(go.Scatter(
                                x = group.exercise,
                                y = group.disaggregated_fit,
                                showlegend = False,
                                marker_color = "red"
                        ))
        return fig

def get_table(results: dict[str, dict], segregated):
        if not segregated:
                results = results["aggregated"]
                beta = results["beta_2"]
                p_value = results["p_value"]
                results_table = pd.DataFrame({
                        "Age Group": ["[10 - 50]"],
                        "Estimate": [beta],
                        "Pr(>|t|)": [p_value]
                })
                return results_table
        age_group = []
        beta = []
        p_value = []
        results = results["segregated"]
        for age, measures in results.items():
                age_group.append(age)
                p_value.append(measures["p_value"])
                beta.append(measures["beta_2"])
        results_table = pd.DataFrame({
                "Age Group": age_group,
                "Estimate": beta,
                "Pr(>|t|)": p_value
        })
        return results_table