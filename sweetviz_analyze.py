import pandas as pd
import sweetviz as sv
import sys

file_path = sys.argv[1]

df = pd.read_csv(file_path, delimiter="^", encoding="utf-8", low_memory=False, error_bad_lines=False)

report = sv.analyze(df, pairwise_analysis="on")
report.show_html(filepath=f'sweetviz_{sys.argv[1].split(".")[0]}.html')