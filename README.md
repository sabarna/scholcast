
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

3. **Navigate to the Project Directory:**
   
    cd scholcast
4. **Create & Activate a Virtual Environment:**
   
    python3 -m venv scholcast_venv
    source scholcast_venv/bin/activate
5. **Install Dependencies:**
   
    pip install -r requirements.txt
6. **Add API Keys in config/config.json**
   
{
    "mathpix_api_id": "YOUR_MATHPIX_API_ID_HERE", <br>
    "mathpix_api_key": "YOUR_MATHPIX_API_KEY_HERE",<br>
    "openai_api_key": "YOUR_OPENAI_API_KEY_HERE"
}

     

### Usage

python src/scholify_pdf.py /path/to/your/document.pdf --output_path output/sample_output/ --format video

**Input Parameters**
1. --input_path: The path to the input PDF file
2. --output_path: The directory where the output files will be saved
3. --format: The desired output format (e.g., audio /video)

**Directory Structure**
   1. README.md: This file.
   2. requirements.txt: List of dependencies required by the project.
   3. src: Source code directory.
   4. av_generator.py: Script for generating audio and video.
   5. candidate_llms: Large Language Models (LLMs) candidates.
   6. config: Configuration files.
   7. logs: Folder got Log files.
   8. output: Directory for output files.
   9. pdf_converter.py: Script for converting PDFs to Latex.
   10. scholify_pdf.py: Main script for converting PDFs to videos.
   11. utils.py: Utility functions.

**Dependencies**

The project relies on several dependencies listed in requirements.txt.

**Contributing**

Contributions are welcome. Here are some steps to contribute:
- Fork the repository.
- Create a new branch for your feature or bug fix.
- Commit your changes with a meaningful commit message.
- Open a pull request.

**License**

Scholcast is released under the MIT License.
