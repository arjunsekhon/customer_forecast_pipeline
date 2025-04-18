"""
Main orchestrator for the Customer Forecast Pipeline.
Runs each stage in sequence: ingest → transform → forecast → optimise → load.
"""
from ingest import ingest
from transform import transform
from forecast import forecast
from optimise import optimise
# from load import load


def main():
    print("Starting full pipeline: ingest → transform → forecast → optimise → load")
    ingest()
    transform()
    forecast()
    optimise()
    # load()
    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()