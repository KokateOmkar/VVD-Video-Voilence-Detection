# Video Violence Detection (VVD)

**A real-time video analysis application that detects violence in videos using deep learning techniques.** This project utilizes advanced machine learning models to analyze video content and provide insights on potential violent actions.

## Features

- **Video Upload**: Users can upload videos for analysis.
- **Real-time Detection**: The application processes videos and detects violence while providing real-time updates on the progress.
- **Annotated Video Output**: The output includes an annotated video highlighting the detected violent actions.
- **WebSocket Support**: Provides real-time communication and progress updates during video processing.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: FastAPI
- **Deep Learning Framework**: PyTorch (for violence detection model)
- **WebSockets**: For real-time updates

## Getting Started

### Prerequisites

- Python 3.7+
- FastAPI
- PyTorch
- WebSocket support
- Other required libraries specified in ```requirements.txt```

### Installation

1. Clone the repository:

   ``` git clone https://github.com/KokateOmkar/VVD-Video-Voilence-Detection.git ```
   
   ``` cd VVD-Video-Voilence-Detection ```

3. Install dependencies:

   ``` pip install -r requirements.txt ```

4. Run the FastAPI application:

   ``` uvicorn main:app --reload ```

5. Open your browser and go to ```http://127.0.0.1:8000``` to access the application.

### Usage

1. Upload a video using the provided form.
2. Monitor the progress bar for real-time updates.
3. View the results, including the annotated video and violence detection information.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (``` git checkout -b feature-branch ```).
3. Make your changes and commit them (``` git commit -m 'Add some feature'```).
4. Push to the branch (``` git push origin feature-branch ```).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [OpenCV](https://opencv.org/) - For video processing.
- [FastAPI](https://fastapi.tiangolo.com/) - For building the web application.
- [PyTorch](https://pytorch.org/) - For deep learning model development.
