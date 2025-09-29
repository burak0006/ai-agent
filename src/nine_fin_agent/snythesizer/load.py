from langchain.docstore.document import Document
from pathlib import Path
import argparse
import logging
import json

from src.nine_fin_agent.snythesizer.builder import synthesize_documents

############# DOCUMENT SYNTHESISE FROM FINANCIAL DATA ################

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).resolve().parents[3]
DEFAULT_INPUT  = ROOT_DIR / "data" / "financial_data.json"
DEFAULT_OUTPUT = ROOT_DIR / "data" / "documents.json"
DEFAULT_SHOW = 10


def run_pipeline(input_path: Path, output_path: Path, show: int = DEFAULT_SHOW):
    """Document Synthesize Pipeline from Financial Json Data"""
    logger.info(f"Loading input file: {input_path}")
    with open(input_path, "r") as f:
        raw_data = json.load(f)

    docs: list[Document] = synthesize_documents(raw_data)
    logger.info(f"Generated {len(docs)} documents")
    print(f"Generated {len(docs)} documents")

    logger.info(f"Showing first {min(show, len(docs))} docs for inspection:")
    for d in docs[:show]:
        print(d.page_content)
        if d.metadata:
            print(f"   metadata: {d.metadata}")
        print("---")

    logger.info(f"Saving output to {output_path}")
    with open(output_path, "w") as f:
        json.dump(
            [{"text": d.page_content, "metadata": d.metadata} for d in docs],
            f,
            indent=2
        )

    logger.info(f"Finished writing {len(docs)} docs")


def main():
    parser = argparse.ArgumentParser(description="Synthesize financial data into text documents.")
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Path to input JSON (default: {DEFAULT_INPUT})"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Path to save synthesized text (default: {DEFAULT_OUTPUT})"
    )
    parser.add_argument(
        "--show",
        type=int,
        default=DEFAULT_SHOW,
        help=f"Number of sample docs to print (default: {DEFAULT_SHOW})"
    )
    args = parser.parse_args()
    run_pipeline(args.input, args.output, args.show)

# REDUNDANT CODE FOR LOCAL TESTING

#if __name__ == "__main__":
#    main()

# python -m src.nine_fin_agent.snythesizer.load --input data/financial_data.json --output data/synthesized.json --show 5