# Copyright 2023 parkminwoo
import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import config as CONF
from datetime import datetime
from src.utils.uitl import add_watermark

formatted_date = datetime.now().strftime("%Y%m%d")
save_path = f"{CONF.SAVE_PATH}/{formatted_date}"


def vis_totalplot(df: pd.DataFrame, enhance_tick: bool = None) -> None:
    """
    Generates a visualization comparing the performance of different Open source LLM models.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to be plotted.
        enhance_tick (bool, optional): Specifies whether to enhance the x-axis ticks based on model names. 
                                       Defaults to None.

    Returns:
        None: The function plots the data and saves the figure.

    """
    sns.set_style("whitegrid")
    _, ax = plt.subplots(figsize=(30, 20))

    metrics = CONF.METRIC_COL
    colors = sns.color_palette("Set2", len(metrics))

    # Plot the metrics for each model
    for i, metric in enumerate(metrics):
        ax.plot(
            df["Model"],
            df[metric],
            marker="o",
            markersize=8,
            color=colors[i],
            label=metric,
        )

    parameters_exist = df[df["Parameters"] != ""]
    if not parameters_exist.empty:
        # Plot the parameter data if available
        ax.plot(
            df["Model"],
            df["Parameters"],
            marker="o",
            markersize=8,
            color="black",
            linestyle="--",
            label="Parameters",
        )

    # Add text labels for the metric values
    for i, model in enumerate(df["Model"]):
        for metric in metrics:
            value = df.loc[df["Model"] == model, metric].values[0]
            ax.text(i, value, str(value), ha="center", va="bottom", size=13)

    # Enhance tick labels based on model names if specified
    if enhance_tick:
        for tick in ax.get_xticklabels():
            label = tick.get_text()
            if re.search(r"(GPT|gpt)", label, flags=re.IGNORECASE):
                tick.set_color("blue")
            if re.search(r"(stable|Stable)", label):
                tick.set_color("red")

    plt.xticks(rotation=45, ha="right", fontsize=20)
    plt.xlabel("Model", fontsize=24)
    plt.ylabel("Score", fontsize=24)
    plt.title("All Open source LLM Model Performance Comparison", fontsize=30)
    plt.legend(prop={"size": 20})
    plt.subplots_adjust(bottom=0.15)

    # Add watermark text
    text = add_watermark()
    plt.text(
        0.5,
        0.4,
        text,
        transform=plt.gcf().transFigure,
        fontsize=30,
        ha="center",
        alpha=0.3,
    )

    ax.invert_xaxis()
    plt.tight_layout()
    plt.savefig(f"{save_path}/totalplot.png", dpi=300)


def vis_rankingplot(df: pd.DataFrame, target_col: str) -> None:
    """
    Visualizes the ranking of open-source LLM models based on a target column.

    Args:
        df (pd.DataFrame): The DataFrame containing the model data.
        target_col (str): The target column to rank the models by.

    Returns:
        None
    """
    df_ranking = df.sort_values(by=target_col, ascending=True)

    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(20, 15))
    colors = sns.color_palette("Set2", len(df_ranking))

    ax.barh(range(len(df_ranking)), df_ranking[target_col], color=colors)

    for i, (model, col) in enumerate(zip(df_ranking["Model"], df_ranking[target_col])):
        ax.text(col, i, model, ha="left", va="center", fontsize=10)

    plt.xlabel(target_col, fontsize=12)
    plt.ylabel("Model", fontsize=12)
    plt.title(f"Open Source LLM Model Ranking by {target_col}", fontsize=30)
    plt.xticks(fontsize=15)
    plt.yticks(range(len(df_ranking)), df_ranking["Model"], fontsize=10)

    text = add_watermark()
    plt.text(
        0.5,
        0.5,
        text,
        transform=plt.gcf().transFigure,
        fontsize=20,
        ha="center",
        alpha=0.4,
    )

    plt.tight_layout()

    plt.savefig(f"{save_path}/rankingplot_{target_col}.png", dpi=300)


def vis_barplot(df: pd.DataFrame, target_col: str) -> None:
    """
    Visualizes the performance comparison of LLM models using a bar plot.

    Args:
        df (pd.DataFrame): The DataFrame containing the model data.
        target_col (str): The target column representing the metric for comparison.

    Returns:
        None
    """
    sns.set_style("whitegrid")
    plt.figure(figsize=(15, 10))
    bars = plt.bar(df["Model"], df[target_col], color="gray")
    highlight_color = "orange"
    for i in range(6):
        bars[i].set_color(highlight_color)
    plt.title(f"LLM Model Performance Comparison, Metric: {target_col}")
    plt.xlabel("Model")
    plt.ylabel(target_col)
    plt.xticks(rotation=45, ha="right")
    plt.gca().invert_xaxis()
    text = add_watermark()
    plt.text(
        0.5,
        0.5,
        text,
        transform=plt.gcf().transFigure,
        fontsize=20,
        ha="center",
        alpha=0.4,
    )
    plt.tight_layout()
    plt.savefig(f"{save_path}/{target_col}.png", dpi=300)


def vis_top10lineplot(df: pd.DataFrame) -> None:
    """
    Visualizes the performance comparison of the top 10 Open source LLM models using a line plot.

    Args:
        df (pd.DataFrame): The DataFrame containing the model data.

    Returns:
        None
    """
    top_10_models = df.nlargest(10, "Average")
    sns.set_style("whitegrid")
    _, ax = plt.subplots(figsize=(14, 8))
    metrics = CONF.METRIC_COL
    colors = sns.color_palette("pastel", len(metrics))
    for i, metric in enumerate(metrics):
        ax.plot(
            top_10_models["Model"],
            top_10_models[metric],
            marker="o",
            markersize=5,
            color=colors[i],
            label=metric,
        )
    parameters_exist = top_10_models[top_10_models["Parameters"] != ""]
    if not parameters_exist.empty:
        ax.plot(
            parameters_exist["Model"],
            parameters_exist["Parameters"],
            marker="o",
            markersize=5,
            color="black",
            linestyle="--",
            label="Parameters",
        )
    for i, model in enumerate(top_10_models["Model"]):
        for j, metric in enumerate(metrics):
            ax.text(
                i,
                top_10_models.loc[top_10_models["Model"] == model, metric].values[0],
                str(
                    top_10_models.loc[top_10_models["Model"] == model, metric].values[0]
                ),
                ha="center",
                va="bottom",
            )
    plt.xticks(rotation=45, ha="right", fontsize=13)
    plt.xlabel("Model", fontsize=10)
    plt.ylabel("Score", fontsize=10)
    plt.title("Top 10 Open source LLM Models Performance Comparison", fontsize=14)
    plt.legend()
    plt.subplots_adjust(bottom=0.15)

    text = text = add_watermark()
    plt.text(
        0.5,
        0.5,
        text,
        transform=plt.gcf().transFigure,
        fontsize=20,
        ha="center",
        alpha=0.4,
    )
    plt.gca().invert_xaxis()
    plt.tight_layout()
    plt.savefig(f"{save_path}/top10_with_lineplot.png", dpi=300)


def vis_top10barplot(df: pd.DataFrame) -> None:
    """
    Visualizes the performance comparison of the top 10 Open source LLM models using a bar plot.

    Args:
        df (pd.DataFrame): The DataFrame containing the model data.

    Returns:
        None
    """
    top_10_models = df.nlargest(10, "Average")
    sns.set_style("whitegrid")
    _, ax = plt.subplots(figsize=(14, 8))
    metrics = CONF.METRIC_COL
    metrics.sort(
        key=lambda x: top_10_models.loc[0, x], reverse=True
    )  # Sort by 'Average' in descending order
    colors = sns.color_palette("pastel", len(metrics))
    for i, metric in enumerate(metrics):
        ax.bar(
            top_10_models["Model"], top_10_models[metric], color=colors[i], label=metric
        )
    parameters_exist = top_10_models[top_10_models["Parameters"] != ""]
    if not parameters_exist.empty:
        ax.plot(
            parameters_exist["Model"],
            parameters_exist["Parameters"],
            marker="o",
            markersize=5,
            color="black",
            linestyle="--",
            label="Parameters",
        )
    for i, model in enumerate(top_10_models["Model"]):
        for j, metric in enumerate(metrics):
            ax.text(
                i,
                top_10_models.loc[top_10_models["Model"] == model, metric].values[0],
                str(
                    top_10_models.loc[top_10_models["Model"] == model, metric].values[0]
                ),
                ha="center",
                va="bottom",
            )
    plt.xticks(rotation=45, ha="right", fontsize=13)
    plt.xlabel("Model", fontsize=12)
    plt.ylabel("Score", fontsize=12)
    plt.title("Top 10 Open source LLM Models Performance Comparison", fontsize=14)
    plt.legend()
    plt.subplots_adjust(bottom=0.15)

    text = add_watermark()
    plt.text(
        0.5,
        0.5,
        text,
        transform=plt.gcf().transFigure,
        fontsize=20,
        ha="center",
        alpha=0.4,
    )
    plt.gca().invert_xaxis()
    plt.tight_layout()
    plt.savefig(f"{save_path}/top10_with_barplot.png", dpi=300)


def vis_top10eachbarplot(df: pd.DataFrame) -> None:
    """
    Visualizes the performance comparison of the top 10 Open source LLM models using separate bars for each metric.

    Args:
        df (pd.DataFrame): The DataFrame containing the model data.

    Returns:
        None
    """
    top_10_models = df.nlargest(10, "Average")
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(14, 8))
    metrics = CONF.METRIC_COL
    colors = sns.color_palette("pastel", len(metrics))

    model_indices = range(len(top_10_models))
    bar_width = 0.15
    for i, metric in enumerate(metrics):
        ax.bar(
            [idx + i * bar_width for idx in model_indices],
            top_10_models[metric],
            width=bar_width,
            color=colors[i],
            label=metric,
        )

    parameters_exist = top_10_models[top_10_models["Parameters"] != ""]
    if not parameters_exist.empty:
        ax.plot(
            parameters_exist["Model"],
            parameters_exist["Parameters"],
            marker="o",
            markersize=5,
            color="black",
            linestyle="--",
            label="Parameters",
        )

    for i, model in enumerate(top_10_models["Model"]):
        for j, metric in enumerate(metrics):
            ax.text(
                i + j * bar_width,
                top_10_models.loc[top_10_models["Model"] == model, metric].values[0],
                str(
                    top_10_models.loc[top_10_models["Model"] == model, metric].values[0]
                ),
                ha="center",
                va="bottom",
            )

    plt.xticks(
        [idx + (len(metrics) - 1) * bar_width / 2 for idx in model_indices],
        top_10_models["Model"],
        rotation=45,
        ha="right",
        fontsize=13,
    )
    plt.xlabel("Model", fontsize=12)
    plt.ylabel("Score", fontsize=12)
    plt.title("Top 10 Open source LLM Models Performance Comparison", fontsize=14)
    plt.legend()
    plt.subplots_adjust(bottom=0.15)

    text = add_watermark()
    plt.text(
        0.5,
        0.5,
        text,
        transform=plt.gcf().transFigure,
        fontsize=20,
        ha="center",
        alpha=0.4,
    )
    plt.gca().invert_xaxis()
    plt.tight_layout()
    plt.savefig(f"{save_path}//top10_with_eachbarplot.png", dpi=300)


def vis_corrheatmap(df: pd.DataFrame) -> None:
    """
    Visualizes the correlation heatmap of the Open source LLM model performance.

    Args:
        df (pd.DataFrame): The DataFrame containing the model data.

    Returns:
        None
    """
    heatmap_data = df[CONF.METRIC_COL]
    heatmap_data = pd.DataFrame(heatmap_data)
    heatmap_data.fillna(0, inplace=True)
    corr_matrix = heatmap_data.corr()
    plt.figure(figsize=(10, 8))

    # Create a mask to hide the upper triangle

    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    text = add_watermark()
    plt.text(
        0.5,
        0.5,
        text,
        transform=plt.gcf().transFigure,
        fontsize=20,
        ha="center",
        alpha=0.4,
    )
    plt.title("Correlation Heatmap of Open source LLM Model Performance")
    plt.tight_layout()
    plt.savefig(f"{save_path}/heatmap.png", dpi=300)


def vis_top5plot(df: pd.DataFrame) -> None:
    """
    Visualizes the top 5 Open source LLM model performance.

    Args:
        df (pd.DataFrame): The DataFrame containing the model data.

    Returns:
        None
    """
    df = pd.DataFrame(df, columns=CONF.WHOLE_COLS,)
    performance_cols = df.columns[2:]
    df[performance_cols] = df[performance_cols].round(1)
    metrics = CONF.METRIC_COL
    colors = sns.color_palette("flare", len(metrics))
    sns.color_palette("flare", 9)
    df = df.set_index("Model")
    df = df.rename_axis("Model", axis="index")
    df.columns.name = "Metrics"
    df_top5 = df.head(5)
    df_top5 = df_top5[df_top5.columns].apply(lambda x: sorted(x, reverse=True)).T
    ax = df_top5.T.plot(
        kind="bar", figsize=(13, 10), rot=0, color=colors, width=0.8, edgecolor="white"
    )
    plt.xlabel("", fontsize=12)
    plt.ylabel("Performance", fontsize=12)
    plt.title("Top 5 Open source LLM Model Performance", fontsize=14)

    creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    plt.text(
        0.99,
        0.99,
        f"Created at: {creation_time}\n github.com/dsdanielpark",
        horizontalalignment="right",
        verticalalignment="bottom",
        transform=ax.transAxes,
        fontsize=10,
        color="gray",
    )

    text = add_watermark()
    plt.text(
        0.5,
        0.5,
        text,
        transform=plt.gcf().transFigure,
        fontsize=20,
        ha="center",
        alpha=0.4,
    )

    plt.xticks(
        range(len(df_top5.columns)),
        df_top5.columns,
        fontsize=20,
        rotation=45,
        ha="right",
    )

    plt.legend(loc="lower right")
    plt.gca().invert_xaxis()
    plt.tight_layout()
    plt.savefig(f"{save_path}/top5plot.png", dpi=300)



def vis_radial_chart(df: pd.DataFrame):
    """
    Create a radial chart (spider or radar chart) based on the provided DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing model names and performance scores for each category.

    Returns:
        None: The function plots the radial chart and saves it as "out.png".

    Note:
        The function assumes that the input DataFrame contains model names in the 'Model' column, and performance scores
        for each category ('Average', 'ARC(25-shot)', 'HellaSwag(10-shot)', 'MMLU(5-shot)', 'TruthfulQA(0-shot)')
        in the corresponding columns. The scores are scaled to range from 1 (minimum) to 5 (maximum) for visual clarity.

        The function will save the radial chart as "out.png" with a resolution of 300dpi.
    """

    # Scaling scores to range from 1 to 5
    for col in df.columns[1:-1]:
        max_val = df[col].max()
        min_val = df[col].min()
        df[col] = ((df[col] - min_val) / (max_val - min_val) * 4) + 1

    # Extracting the top 5 models based on the 'Average' score
    top_5_models = df.nlargest(5, 'Average')

    # Creating the radial chart
    categories = list(df.columns[1:-1])
    categories.remove("Parameters")
    N = len(categories)

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    _, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), dpi=300)

    # Setting colors for the top 5 models
    cmap = plt.get_cmap('Set2')
    colors = cmap(np.linspace(0, 1, len(top_5_models)))

    # Plotting the radar chart for each top 5 model
    for i, model in enumerate(top_5_models.iterrows()):
        values = model[1][categories].tolist()
        values += values[:1]
        rank_label = f"{i+1}st"
        ax.plot(angles, values, label=f"{rank_label} - {model[1]['Model']}", linestyle='--', color=colors[i], linewidth=2)
        ax.fill(angles, values, alpha=0.1, color=colors[i])

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(0)

    # Setting axis labels and ticks
    plt.xticks(angles[:-1], categories, fontsize=12, rotation=45)
    ax.set_rlabel_position(45)
    plt.yticks([1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"], color="grey", size=10)
    plt.ylim(1, 5.3)

    # Adding chart title and legend
    plt.title("Top 5 Open LLM Radial Plot", fontsize=20)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    plt.text(
        0.99,
        0.99,
        f"Created at: {creation_time}\n github.com/dsdanielpark",
        horizontalalignment="right",
        verticalalignment="bottom",
        transform=ax.transAxes,
        fontsize=10,
        color="gray",
    )

    # Adding descriptive text below the chart
    plt.text(0.7, -0.1, "The minimum score of each category is scaled to 1, and the maximum score is scaled to 5. \n You can see more plots at https://github.com/dsdanielpark/open-llm-leaderboard-report",
             fontsize=10, ha='center', va='center', transform=plt.gca().transAxes)

    plt.savefig(f"{save_path}/radial_chart.png", dpi=300, bbox_inches='tight')
    plt.close()
