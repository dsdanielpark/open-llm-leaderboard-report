
from datetime import datetime


def add_watermark():
    creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    github_link = "github.com/dsdanielpark"
    text = f"Created on: {creation_time}\n{github_link}"

    return text