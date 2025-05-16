# UUID Format Converter

A GUI utility for converting UUIDs between different formats.

## Features

- Convert UUIDs between multiple formats:
  - Standard UUID format with hyphens (e.g., `904ca0c8-54b7-42da-81a7-4bed2d89fa29`)
  - Uppercase without hyphens (e.g., `904CA0C854B742DA81A74BED2D89FA29`)
  - Hex format with 0x prefix (e.g., `0x904CA0C854B742DA81A74BED2D89FA29`)
  - Python bytes representation (e.g., `b'\x90L\xa0\xc8T\xb7B\xda\x81\xa7K\xed-\x89\xfa)'`)
- Batch processing: Convert multiple UUIDs at once
- Extract UUIDs from URLs or text
- Toggle between newline and comma-separated output formats
- Copy results to clipboard with one click

## Installation

1. Make sure you have Python 3.11 or newer installed
2. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/vibe-hex.git
   cd vibe-hex
   ```
4. Install dependencies:
   ```bash
   poetry install
   ```

## Usage

Run the application using Poetry:
```bash
poetry run hex
```

Or activate the virtual environment and run directly:
```bash
poetry shell
hex
```

## Input Formats Supported

The converter accepts:
- Standard UUIDs with or without hyphens
- UUIDs in URLs or other text
- Python byte string representations
- Hex format with 0x prefix

Simply paste your input in any of these formats and click "Convert" to see all format variations.
