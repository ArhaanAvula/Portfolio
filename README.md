# AI-Powered Phishing URL Detection Chrome Extension

A machine learning-based Chrome extension designed to help users identify potentially malicious URLs and recognize online threats.

## Overview

I developed this project after seeing how phishing scams and suspicious links could compromise people's online accounts. I wanted to build an accessible tool that could help users identify potentially malicious links before interacting with them.

The extension combines a Chrome browser interface with a Python Flask backend and a LightGBM machine learning model to evaluate URLs. The goal is to make suspicious links easier to recognize through a simple, user-friendly experience.

## Features

- **URL Classification:** Uses a trained LightGBM model to classify URLs as potentially malicious or benign.
- **Chrome Extension Integration:** Connects browser functionality to a Python-based prediction backend.
- **Visual Warnings:** Designed to highlight suspicious links on webpages so users can more easily identify potential threats.
- **Machine Learning:** Applies data-driven pattern recognition to distinguish potentially malicious URLs from legitimate ones.

## Technologies Used

- **Python** for model development and backend logic
- **LightGBM** for machine learning-based URL classification
- **Flask** for communication between the extension and the prediction backend
- **JavaScript** for browser interaction and webpage link handling
- **HTML, CSS, and Chrome Extension APIs** for the browser interface and functionality, where applicable

## Model Evaluation

During testing, the model achieved the following reported results:

| Metric | Result |
|---|---:|
| Accuracy | 93.07% |
| Recall (True Positive Rate) | 69.91% |
| Precision | 79.65% |
| False Positive Rate | 3.02% |

These results reflect the model's evaluation on the dataset used during development. Performance on new, real-world URLs may differ.

An important part of this project was balancing overall accuracy with the ability to detect malicious links. While tuning the model, I considered the tradeoff between correctly identifying threats and incorrectly flagging legitimate URLs. The results reinforced that no classification model is perfect, and false negatives remain a limitation.

## How It Works

1. A user activates the Chrome extension on a webpage.
2. The extension identifies links for evaluation.
3. URLs are sent to the Flask backend for prediction.
4. The LightGBM model evaluates the URLs and returns classifications.
5. The extension can use those results to highlight potentially suspicious links.

The exact workflow depends on the extension and backend configuration.

## Project Goals

This project explores how machine learning can be applied to cybersecurity in a way that is accessible to everyday users. Rather than requiring users to understand technical URL indicators themselves, the extension aims to make potential risks easier to recognize.

## Recognition

This project was submitted to the Congressional App Challenge and received a **Certificate of Special Recognition from Representative Mark DeSaulnier**.

## Limitations

- The model may incorrectly classify legitimate URLs or fail to identify malicious ones.
- Evaluation metrics do not guarantee the same performance on real-world traffic.
- The extension should be treated as a supplementary security tool, not a guarantee that a webpage or link is safe.
- The prediction backend must be running and correctly configured for the extension to communicate with it.

## Future Improvements

Potential improvements include expanding evaluation to more diverse URL datasets, improving detection performance, refining the user interface, and making backend setup and deployment easier.

## Author

Developed by Arhaan Avula as an independent cybersecurity and machine learning project.
