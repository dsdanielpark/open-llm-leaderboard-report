import os
import json
import config as CONF
from datetime import datetime
from src.plotting.vis_plotter import *
from src.processing.preprocessor import run_preprocess


def run_steps(step_names: list) -> None:

    # Set date and save path
    now = datetime.now()
    formatted_date = now.strftime("%Y%m%d")
    save_path = f"{CONF.SAVE_PATH}/{formatted_date}"
    os.makedirs(save_path, exist_ok=True)
    formatted_date = datetime.now().strftime("%Y%m%d")
    data_path = f"{CONF.DATA_PATH}/{formatted_date}.json"
    print(f"\n* Plots will be made using {data_path}")

    # Open raw data
    with open(data_path, "r") as f:
        data = json.load(f)
    df = run_preprocess(data)  # Assuming you have a run_preprocess function
    df.to_csv(f"{save_path}/{formatted_date}.csv", index=False, encoding="utf-8-sig")

    # Set metric col
    metrics = CONF.METRIC_COL

    # Set max model number to plot
    df = df.iloc[: CONF.N_MODEL]
    df = df.sort_values(by="Average", ascending=False)
    df = df.drop_duplicates(subset="Model", keep="first")

    # Run steps
    for name in step_names:
        if name == "vis_totalplot":
            vis_totalplot(df, False)
        elif name == "vis_corrheatmap":
            vis_corrheatmap(df)
        elif name == "vis_barplot":
            for col in metrics:
                vis_barplot(df, col)
        elif name == "vis_rankingplot":
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
