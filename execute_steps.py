import os
from datetime import datetime
import json
import config as CONF
from src.plotting.vis_plotter import *
from src.processing.preprocessor import run_preprocess

def run_steps(step_names):
    now = datetime.now()
    formatted_date = now.strftime("%Y%m%d")
    save_path = f'{CONF.SAVE_PATH}/{formatted_date}'
    os.makedirs(save_path, exist_ok=True)
    formatted_date = datetime.now().strftime("%Y%m%d")
    data_path = f"{CONF.DATA_PATH}/{formatted_date}.json"
    print(f"\n* Plots will be made using {data_path}")
    
    with open(data_path, "r") as f:
        data = json.load(f)
    df = run_preprocess(data)  # Assuming you have a run_preprocess function
    df.to_csv(f"{save_path}/{formatted_date}.csv", index=False, encoding="utf-8-sig")

    for name in step_names:
        if name == "vis_totalplot":
            vis_totalplot(df, False)
        elif name == "vis_corrheatmap":
            vis_corrheatmap(df)
        elif name == "vis_barplot":
            metrics = ["Average", "ARC (25-shot)", "HellaSwag (10-shot)", "MMLU (5-shot)", "TruthfulQA (0-shot)", "Parameters"]
            for col in metrics:
                vis_barplot(df, col)
        elif name == "vis_rankingplot":
            metrics = ["Average", "ARC (25-shot)", "HellaSwag (10-shot)", "MMLU (5-shot)", "TruthfulQA (0-shot)", "Parameters"]
            for col in metrics:
                vis_rankingplot(df, col)
        elif name == "vis_top10lineplot":
            vis_top10lineplot(df)
        elif name == "vis_top10barplot":
            vis_top10barplot(df)
        elif name == "vis_top5plot":
            vis_top5plot(df)
        elif name == "vis_totalplot_all":
            vis_totalplot(df)
        elif name == "vis_totalplot_enhanced":
            vis_totalplot(df, True)
        else:
            print(f"Invalid step name: {name}. Skipping this step.")

