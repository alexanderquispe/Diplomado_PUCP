import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
import pandas as pd

def generate_data(n = 1000):
        avg_age_group = np.random.choice([10, 20, 30, 40, 50], size = (n, 1))
        exercise_mean = 10
        exercise_sd = 15
        cholesterol_mean = 130
        cholesterol_sd = 15
        effect_age_on_exercise = 4
        effect_age_on_cholesterol = 4
        exercise = np.random.normal(exercise_mean, exercise_sd, size = (n, 1)) + effect_age_on_exercise * avg_age_group
        cholesterol = np.random.normal(cholesterol_mean, cholesterol_sd, size = (n, 1)) + (-0.5) * exercise + avg_age_group * effect_age_on_cholesterol
        data = pd.DataFrame({"exercise": exercise.reshape(n), "cholesterol": cholesterol.reshape(n), "age_groups": avg_age_group.reshape(n).astype(str)})
        return data

def bivariate_regression(data, outcome_label, explanatory_label):
        n = data.shape[0]
        outcome = data[outcome_label].to_numpy().reshape((n, 1))
        explanatory = data[explanatory_label].to_numpy().reshape((n, 1))
        mean_outcome = outcome.mean()
        mean_explanatory = explanatory.mean()
        outcome_deviations = outcome - mean_outcome
        explanatory_deviations = explanatory - mean_explanatory
        beta_2 = (outcome_deviations * explanatory_deviations).sum() / (explanatory_deviations ** 2).sum()
        beta_1 = mean_outcome - mean_explanatory * beta_2
        error_deviations = outcome_deviations - explanatory_deviations * beta_2
        estimated_variance = (error_deviations ** 2).sum() / (n - 2)
        beta_2_variance = estimated_variance / (explanatory_deviations ** 2).sum()
        return beta_1, beta_2, beta_2_variance

def calculate_pvalue(beta, beta_variance):
        t_statistic = beta / np.sqrt(beta_variance)
        p_value = 2 * norm.cdf(-np.abs(t_statistic))
        return p_value

def regression_results(data, outcome_label, explanatory_label):
        beta_1, beta_2, beta_2_variance = bivariate_regression(data, outcome_label, explanatory_label)
        p_value = calculate_pvalue(beta_2, beta_2_variance)
        results = {
                "beta_1": beta_1,
                "beta_2": beta_2, 
                "p_value": p_value
        }
        return results

def disaggregated_fits(data, explanatory_label, group_variable, results):
        data["disaggregated_beta1"] = data[group_variable].apply(lambda row: results[row]["beta_1"])
        data["disaggregated_beta2"] = data[group_variable].apply(lambda row: results[row]["beta_2"])
        disaggregated_fit = data["disaggregated_beta1"] + data["disaggregated_beta2"] * data[explanatory_label]
        return disaggregated_fit


def execute_regressions(data: pd.DataFrame, outcome_label = "cholesterol", explanatory_label = "exercise", group_variable = "age_groups"):
        results = {
                "segregated": {}, 
                "aggregated": regression_results(data, outcome_label, explanatory_label)
        }
        for age, group in data.groupby(group_variable):
                results["segregated"].update({age: regression_results(group, outcome_label, explanatory_label)})
        aggregated = results["aggregated"]
        data["aggregated_fit"] = aggregated["beta_1"] + aggregated["beta_2"] * data[explanatory_label]
        data["disaggregated_fit"] = disaggregated_fits(data, explanatory_label, group_variable, results["segregated"])
        return results, data



