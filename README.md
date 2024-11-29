
# Scholcast

## Overview
Scholcast is a project designed to convert academic papers and other documents into various formats, including videos, using advanced natural language processing and multimedia tools.

## Installation

### Prerequisites
- Python 3.13 or later
- A compatible operating system (tested on macOS)

### Setting Up the Environment

1. **Clone the Repository:**
   git clone https://github.com/sabarna/scholcast.git

2. **Navigate to the Project Directory:**
    cd scholcast
3. **Create & Activate a Virtual Environment:**
    python3 -m venv scholcast_venv
    source scholcast_venv/bin/activate
4. **Install Dependencies:**
    pip install -r requirements.txt

### Usage
python src/scholify_pdf.py /path/to/your/document.pdf --output_path output/sample_output/ --format video

**Input Parameters**
--input_path: The path to the input PDF file
--output_path: The directory where the output files will be saved
--format: The desired output format (e.g., audio /video)

**Directory Structure**
    README.md: This file.
    requirements.txt: List of dependencies required by the project.
    src: Source code directory.
    av_generator.py: Script for generating audio and video.
    candidate_llms: Large Language Models (LLMs) candidates.
    config: Configuration files.
    logs: Log files.
    narrative.txt: Sample narrative text.
    output: Directory for output files.
    pdf_converter.py: Script for converting PDFs.
    scholify_pdf.py: Main script for converting PDFs to videos.
    utils.py: Utility functions.
**Dependencies**
The project relies on several dependencies listed in requirements.txt.

**Contributing**
Contributions are welcome. Here are some steps to contribute:
Fork the repository.
Create a new branch for your feature or bug fix.
Commit your changes with a meaningful commit message.
Open a pull request.

**License**
Scholcast is released under the MIT License.
