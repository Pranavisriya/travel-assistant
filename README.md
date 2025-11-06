# Travel assistant

An agent that helps plan concise, practical travel itineraries with neighborhood tips, cost ranges, and essential visa/safety notes.

## Prerequisites

- Python 3.12 or higher
- uv
- API keys for:
  - Groq


## Installation

1. Clone the repository:
```bash
git clone https://github.com/Pranavisriya/travel-assistant.git
cd travel-assistant
```

2. Create a virtual python environment in this repo
```bash
conda create -p venv python=3.12 -y
```

Any other method can also be used to create python environment.

3. Activate python environment
```bash
conda activate ./venv
```

4. Install `uv` in the environment if it is not present
```bash
pip install uv
```

5. Install dependencies using uv:
```bash
uv add -r requirements.txt
```

6. Create a `.env` file in the project root with your API keys:
```
GROQ_API_KEY=your_groqapi_key
```

## Usage

Run the frontend using app.py:
```bash
streamlit run app.py
```


## Features

- Itinerary builder: Generates short, city-by-city plans based on places you provide.
- Neighborhood & lodging tips: Brief, location-specific suggestions.
- Cost guidance: Typical (non-live) ranges for food, transport, and activities.
- Quick Guide add-on: Visa requirements, best time to visit, highlights by area, getting around, safety & health, and key emergency numbers.


## License

This project is licensed under the terms included in the LICENSE file.

## Author

Pranavi Sriya (pranavisriyavajha9@gmail.com)


