"""Runs the three analyses in order (about one minute; most of it in 03_forecast.py)."""
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
for script in ("01_trend.py", "02_seasonality.py", "03_forecast.py"):
    print(f"Running {script}")
    runpy.run_path(str(HERE / script), run_name="__main__")
print("Done. Figures and tables are in ../figures.")
