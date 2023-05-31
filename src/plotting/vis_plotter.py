import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import re
from datetime import datetime
import config as CONF
import numpy as np
from src.utils.uitl import add_watermark

formatted_date = datetime.now().strftime("%Y%m%d")
save_path = f'{CONF.SAVE_PATH}/{formatted_date}'




def vis_totalplot(df: pd.DataFrame, enhance_tick: bool = None):
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(30, 20))
    
    metrics = ["Average", "ARC (25-shot)", "HellaSwag (10-shot)", "MMLU (5-shot)", "TruthfulQA (0-shot)"]
    colors = sns.color_palette("Set2", len(metrics))
    
    for i, metric in enumerate(metrics):
        ax.plot(df['Model'], df[metric], marker='o', markersize=5, color=colors[i], label=metric)
    
    parameters_exist = df[df['Parameters'] != '']
    if not parameters_exist.empty:
        ax.plot(parameters_exist['Model'], parameters_exist['Parameters'], marker='o', markersize=5, color='black', linestyle='--', label='Parameters')
    
    for i, model in enumerate(df['Model']):
        for j, metric in enumerate(metrics):
            value = df.loc[df['Model'] == model, metric].values[0]
            ax.text(i, value, str(value), ha='center', va='bottom')
    
    if enhance_tick:
        for tick in ax.get_xticklabels():
            label = tick.get_text()
            if re.search(r'(GPT|gpt)', label, flags=re.IGNORECASE):
                tick.set_color('blue')  
            if re.search(r'(stable|Stable)', label):
                tick.set_color('red') 
    
    plt.xticks(rotation=45, ha='right', fontsize=15)
    plt.xlabel('Model', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.title('All Open source LLM Model Performance Comparison', fontsize=30)
    plt.legend()
    plt.subplots_adjust(bottom=0.15)
    
    text = add_watermark()
    plt.text(0.3, 0.8, text, transform=plt.gcf().transFigure, fontsize=20, ha='center', alpha=0.4)
    
    ax.invert_xaxis()  
    plt.tight_layout()
    plt.savefig(f"{save_path}/totalplot.png", dpi=300)




def vis_rankingplot(df, target_col):
    df_ranking = df.sort_values(by=target_col, ascending=True) 

    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(20, 15))
    colors = sns.color_palette("Set2", len(df_ranking))

    ax.barh(range(len(df_ranking)), df_ranking[target_col], color=colors)
    
    for i, (model, col) in enumerate(zip(df_ranking['Model'], df_ranking[target_col])):
        ax.text(col, i, model, ha='left', va='center', fontsize=10)

    plt.xlabel(target_col, fontsize=12)
    plt.ylabel('Model', fontsize=12)
    plt.title(f'Open Source LLM Model Ranking by {target_col}', fontsize=30)
    plt.xticks(fontsize=15)
    plt.yticks(range(len(df_ranking)), df_ranking['Model'], fontsize=10)
    
    text = add_watermark()
    plt.text(0.5, 0.5, text, transform=plt.gcf().transFigure, fontsize=20, ha='center', alpha=0.4)

    plt.savefig(f"{save_path}/rankingplot_{target_col}.png", dpi=300)
    plt.tight_layout()



def vis_barplot(df, col):
    sns.set_style("whitegrid")
    plt.figure(figsize=(15, 10))
    bars = plt.bar(df["Model"], df[col], color="gray")
    highlight_color = "orange"
    for i in range(6):
        bars[i].set_color(highlight_color)
    plt.title(f"LLM Model Performance Comparison, Metric:{col}")
    plt.xlabel("Model")
    plt.ylabel(col)
    plt.xticks(rotation=45, ha="right")
    plt.gca().invert_xaxis()  
    text = add_watermark()
    plt.text(0.5, 0.5, text, transform=plt.gcf().transFigure, fontsize=20, ha='center', alpha=0.4)
    plt.tight_layout()
    plt.savefig(f"{save_path}/{col}.png", dpi=300)




def vis_top10lineplot(df):
    top_10_models = df.nlargest(10, 'Average')
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(14, 8))
    metrics = ["Average", "ARC (25-shot)", "HellaSwag (10-shot)", "MMLU (5-shot)", "TruthfulQA (0-shot)"]
    colors = sns.color_palette("pastel", len(metrics))
    for i, metric in enumerate(metrics):
        ax.plot(top_10_models['Model'], top_10_models[metric], marker='o', markersize=5, color=colors[i], label=metric)
    parameters_exist = top_10_models[top_10_models['Parameters'] != '']
    if not parameters_exist.empty:
        ax.plot(parameters_exist['Model'], parameters_exist['Parameters'], marker='o', markersize=5, color='black', linestyle='--', label='Parameters')
    for i, model in enumerate(top_10_models['Model']):
        for j, metric in enumerate(metrics):
            ax.text(i, top_10_models.loc[top_10_models['Model'] == model, metric].values[0], str(top_10_models.loc[top_10_models['Model'] == model, metric].values[0]), ha='center', va='bottom')
    plt.xticks(rotation=45, ha='right', fontsize=15)
    plt.xlabel('Model', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.title('Top 10 Open source LLM Models Performance Comparison', fontsize=14)
    plt.legend()
    plt.subplots_adjust(bottom=0.15)

    text = text = add_watermark()
    plt.text(0.5, 0.5, text, transform=plt.gcf().transFigure, fontsize=20, ha='center', alpha=0.4)
    plt.gca().invert_xaxis() 
    plt.tight_layout()
    plt.savefig(f"{save_path}/top10_with_lineplot.png", dpi=300)


def vis_top10barplot(df):
    top_10_models = df.nlargest(10, 'Average')
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(14, 8))
    metrics = ["Average", "ARC (25-shot)", "HellaSwag (10-shot)", "MMLU (5-shot)", "TruthfulQA (0-shot)"]
    colors = sns.color_palette("pastel", len(metrics))
    for i, metric in enumerate(metrics):
        ax.bar(top_10_models['Model'], top_10_models[metric], color=colors[i], label=metric)
    parameters_exist = top_10_models[top_10_models['Parameters'] != '']
    if not parameters_exist.empty:
        ax.plot(parameters_exist['Model'], parameters_exist['Parameters'], marker='o', markersize=5, color='black', linestyle='--', label='Parameters')
    for i, model in enumerate(top_10_models['Model']):
        for j, metric in enumerate(metrics):
            ax.text(i, top_10_models.loc[top_10_models['Model'] == model, metric].values[0], str(top_10_models.loc[top_10_models['Model'] == model, metric].values[0]), ha='center', va='bottom')
    plt.xticks(rotation=45, ha='right', fontsize=15)
    plt.xlabel('Model', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.title('Top 10 Open source LLM Models Performance Comparison', fontsize=14)
    plt.legend()
    plt.subplots_adjust(bottom=0.15)
    
    text = text = add_watermark()
    plt.text(0.5, 0.5, text, transform=plt.gcf().transFigure, fontsize=20, ha='center', alpha=0.4)
    plt.gca().invert_xaxis()  
    plt.tight_layout()
    plt.savefig(f"{save_path}//top10_with_barplot.png", dpi=300)




def vis_corrheatmap(df):
    heatmap_data = df[["Average", "ARC (25-shot)", "HellaSwag (10-shot)", "MMLU (5-shot)", "TruthfulQA (0-shot)"]]
    corr_matrix = heatmap_data.corr()
    plt.figure(figsize=(10, 8))
    
    # Create a mask to hide the upper triangle
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, mask=mask)
    text = add_watermark()
    plt.text(0.5, 0.5, text, transform=plt.gcf().transFigure, fontsize=20, ha='center', alpha=0.4)
    plt.title('Correlation Heatmap of Open source LLM Model Performance')
    plt.tight_layout()
    plt.savefig(f"{save_path}/heatmap.png", dpi=300)


def vis_top5plot(df):
    df = pd.DataFrame(df, columns=["Model", "Revision", "Average", "ARC (25-shot)", "HellaSwag (10-shot)", "MMLU (5-shot)", "TruthfulQA (0-shot)"])
    performance_cols = df.columns[2:]
    df[performance_cols] = df[performance_cols].round(1)
    metrics = ["Average", "ARC (25-shot)", "HellaSwag (10-shot)", "MMLU (5-shot)", "TruthfulQA (0-shot)"]
    colors = sns.color_palette("flare", len(metrics))
    sns.color_palette("flare", 9)
    df = df.set_index("Model")
    df = df.rename_axis("Model", axis="index")
    df.columns.name = "Metrics"
    df_top5 = df.head(5)
    df_top5 = df_top5[df_top5.columns].apply(lambda x: sorted(x, reverse=True)).T
    ax = df_top5.T.plot(kind="bar", figsize=(13, 10), rot=0, color=colors, width=0.8, edgecolor="white")
    plt.xlabel("", fontsize=12)
    plt.ylabel("Performance", fontsize=12)
    plt.title("Top 5 Open source LLM Model Performance", fontsize=14)

    creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    plt.text(0.99, 0.99, f"Created at: {creation_time}\n github.com/dsdanielpark",
            horizontalalignment='right', verticalalignment='bottom', transform=ax.transAxes,
            fontsize=10, color='gray')


    text = add_watermark()
    plt.text(0.5, 0.5, text, transform=plt.gcf().transFigure, fontsize=20, ha='center', alpha=0.4)

    plt.xticks(range(len(df_top5.columns)), df_top5.columns, fontsize=20, rotation=45, ha="right")

    plt.legend(loc="lower right")
    plt.gca().invert_xaxis()  
    plt.tight_layout()
    plt.savefig(f"{save_path}/top5plot.png", dpi=300)
