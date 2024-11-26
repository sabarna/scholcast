#!/usr/bin/env python3

import argparse
from pdf_converter import PDFConverter
from candidate_llms.knowledge_graph_llm import PaperAnalyzer
from av_generator import AudioVideoGenerator
from utils import get_title

def main():
    parser = argparse.ArgumentParser(description="Convert PDF papers to audio/video files")
    parser.add_argument("input_file", help="Path to the input PDF file")
    parser.add_argument("--output_path", help="Path to save the output files")
    parser.add_argument("--format", choices=["audio", "video"], default="audio", help="Output format")
    parser.add_argument("--upload_to_youtube", choices=["y", "n"], default="n", help="flag to upload to Youtube")
    args = parser.parse_args()
    pdf_converter = PDFConverter()
    processed_text = pdf_converter.process_pdf(args.input_file)
    title = get_title(processed_text)
    analyzer = PaperAnalyzer()
    narrative = analyzer.get_narrative(processed_text, title)
    generator = AudioVideoGenerator()
    generator.get_av(narrative, args.format, args.output_path)

if __name__ == "__main__":
    main()