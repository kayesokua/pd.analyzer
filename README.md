# pd.analyzer 💃 🕺

pd.analyzer is a work-in-progress application designed to bring the power of data science and machine learning to the art of pole dancing. It aims to create a comprehensive framework for analyzing, summarizing, and enhancing pole dance performances using advanced computational techniques.

## Features

1. Dance Analysis Services & Dashboard
![Sample Dashboard View](https://i.ibb.co/g3crywn/Screenshot-2024-01-07-at-03-36-38.png)

`http://127.0.0.1:5000/dashboard/<username>`

2. Static Pole Dance Dataset
![Sample Pose Data Visualization, Carousel Grip](https://ibb.co/fpTNg6w)

Route for downloading dataset: `http://127.0.0.1:5000/dataset` 

## Structure

```
├── LICENSE
├── README.md
├── app/ # Main application directory.
│   ├── api/ # Module for api endpoints
│   ├── auth/ # Module for account authentication and authorization
│   ├── dashboard/ # Module for dashboard and reports
│   ├── main/ # Main web app module
│   ├── models/ # All data models found in the app
│   ├── services/ # Core services like video processing, pose recognition, and data visualization.
│   ├── static/ # Assets, css, js, icons..
│   └── templates/ # HTML templates for rendering the web interface.
├── data
│   ├── external # Data bucket for pdictionary
│   ├── processed # Data bucket for processed results
│   └── uploads # Data bucket for raw video uploads
│   ..prod.sqlite # Database for web activities and video metadeta
├── migrations
├── requirements # Requirements
├── run.py
├── scripts # Standalone utility scripts
└── tests
```

## Requirements
Python dependencies are listed in `requirements/`. They include Flask for web framework, OpenCV for image processing, and various machine learning libraries.

## Resources
1. Project Template from [Miguel Grinberg's Flask Web Development, 2nd Edition](https://github.com/miguelgrinberg/flasky/)
2. [MediaPipe | Google for Developers](https://github.com/google/mediapipe)
3. [Plotly Python Graphing Library](https://plotly.com/python/)