# DigitDoodle 🖌️

DigitDoodle is a fun and interactive application that lets users draw handwritten digits on a canvas and get instant recognition using a deep learning model. Built with PyQt for a smooth drawing experience and powered by TensorFlow for digit recognition, DigitDoodle demonstrates the practical power of machine learning in an intuitive way.

## demo
<img src="resources/demo.gif" alt="DigitDoodle demo gif" width="600">

## Features

- **Interactive Drawing Canvas**: Use your mouse to draw digits directly on the app's canvas
- **Handwritten Digit Recognition**: The app uses a pre-trained neural network to recognize your drawn digit and displays the prediction
- **Clear and Try Again**: Easily clear the canvas and try with different digits
- **Machine Learning Model**: Powered by a simple yet effective neural network trained on the MNIST dataset

## Project Structure

```
DigitDoodle/
├── data/
│   ├── __init__.py                   # Makes this a package
│   └── dataset_loader.py             # Script to load and preprocess MNIST data
│
├── models/
│   ├── __init__.py                   # Makes this a package
│   ├── digit_recognizer_model.h5     # Saved trained model
│   └── model_builder.py              # Script to define and compile the model
│
├── app/
│   ├── __init__.py                   # Makes this a package
│   ├── main.py                       # Main script to run the PyQt application
│   └── canvas.py                     # PyQt canvas class for drawing
│
├── utils/
│   ├── __init__.py                   # Makes this a package
│   └── helper_functions.py           # Helper functions
│
├── resources/
│   └── README.md                     # Project description
│
├── requirements.txt                  # Required dependencies
└── train.py                         # Script to train and save the model
```

## Getting Started

### Prerequisites

- Python 3.7+
- Virtual environment (optional but recommended)

### Installation

1. **Clone the Repository:**
```bash
git clone https://github.com/your-username/DigitDoodle.git
cd DigitDoodle
```

2. **Set Up a Virtual Environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

### Training the Model (Optional)

To train the model yourself instead of using the provided `digit_recognizer_model.h5` file:

```bash
python train.py
```

### Running the Application

Start the application with:

```bash
python app/main.py
```

## How to Use DigitDoodle

1. **Draw a Digit**: Use your mouse to draw a digit (0-9) on the canvas
2. **Recognize**: Click the "Recognize" button to classify the digit
3. **Clear**: Click "Clear" to reset the canvas and try another digit

## Model Details

The digit recognition model uses a neural network architecture:
- **Input**: 28x28 grayscale image
- **Architecture**:
  - Flatten Layer (784-dimensional vector)
  - Three Dense Layers (128 neurons each, ReLU activation)
  - Output Layer (10 neurons, softmax activation)
- **Training**: MNIST dataset (60,000 training images, 10,000 test images)
- **Loss**: sparse_categorical_crossentropy
- **Optimizer**: adam

## Troubleshooting

- **FileNotFoundError**: Ensure `digit_recognizer_model.h5` exists in the `models/` directory or run `train.py`
- **Model Prediction Errors**: Try drawing digits more clearly and distinctly

## Future Enhancements

- Enhanced Model: Implement CNN for improved accuracy
- Backend Server: Host model on server with API interaction
- Mobile App Version: Touch-based drawing support
- Digit Animation: Add UI animations for recognition events

## Contributing

We welcome contributions! Feel free to:
- Open issues
- Request new features
- Submit pull requests

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Created by [Your Name or Username] – [Your Email or GitHub Link]

Happy Doodling with Digits! 🎨✨
