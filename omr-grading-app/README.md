# OMR Grading App

A Streamlit-based application for grading OMR sheets using an answer key in Excel format.

## Features

- Upload OMR sheet images and answer key
- Automated grading
- View historical results

## Project Structure

```
omr-grading-app/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── setup.sh                  # Setup script (optional)
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── pages/
│   └── 2_History.py          # Additional page for historical results
├── data/
│   └── Key (Set A and B).xlsx  # Your answer key
├── src/
│   ├── answer_key_parser.py
│   ├── database.py
│   └── omr_grading_system.py
├── utils/
│   ├── file_utils.py
│   └── visualization.py
└── README.md
```

## Getting Started

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the app:
   ```sh
   streamlit run app.py
   ```

## License

MIT
