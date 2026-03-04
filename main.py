from data import prepare_data
from math_engine import run_calculations
from ppt import build_master_report

def run_pipeline(master_file):

    df, err = prepare_data(master_file)

    results = run_calculations(df, err)

    ppt_bytes = build_master_report(results)

    return ppt_bytes