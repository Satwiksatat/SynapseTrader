# SynapseTrader

An intelligent trading system powered by AI.

## Project Structure

```
synapse_trader/
├── .gitignore        # Git ignore file
├── README.md         # Project documentation
├── requirements.txt  # Python dependencies
├── .env             # Environment variables (not tracked in git)
├── app.py           # Main application entry point
├── agent.py         # AI agent implementation
├── tools.py         # Trading tools and utilities
│
├── data/            # Trading data storage
│   └── wrds_swap_data.csv
│
├── audio_outputs/   # Generated audio outputs
│   └── .gitkeep
│
└── assets/         # Static assets
    └── logo.png
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env  # Create from template
# Edit .env with your configuration
```

## Usage

[Documentation to be added]

## License

[License information to be added]