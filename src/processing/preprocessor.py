import pandas as pd
import re


def run_preprocess(data):
    df = pd.DataFrame(data, columns=["Model", "Revision", "Average", "ARC (25-shot)", "HellaSwag (10-shot)", "MMLU (5-shot)", "TruthfulQA (0-shot)"])
    df.drop('Revision', axis=1, inplace=True)
    
    df.iloc[:, 2:] = df.iloc[:, 2:].round(1)
    
    pattern = r'(\d+(?:\.\d+)?)([bBmM])'
    df['Parameters'] = df['Model'].apply(lambda model: int(float(re.findall(pattern, model)[0][0]) * (1_000_000_000 if re.findall(pattern, model)[0][1].lower() == 'b' else 1_000_000)) if re.findall(pattern, model) else 0)
    if df['Parameters'].max() != 0:
        df['Parameters'] = (df['Parameters'] / df['Parameters'].max()) * 100
    
    df['URL'] = df['Model'].apply(lambda model: f"https://huggingface.co/{model}" if '/' in model else '')
    
    return df
