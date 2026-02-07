# Spam Detector

A program to determine if a mail is a spam or not

## Description

This application uses Machine Learning technology to find out if a mail is a spam or not. By copying the mail in the app, the program, using technologies such as TF-IDF, Pandas or Torch.
The content of the mail will first be cleaned of any ponctuation or useless words (as per the english stopwords found in the stopwords module of the nltk.corpus library), then will be vectorized into a matrix using Scikit Learn. Finally, using PyTorch's FloatTensor, the matrix's data will be stored in an array, before being passed into the model.

The model works as follow:
The model uses Linear, Rectified Linear Unit (ReLU), and Sigmoid. Linear will give a score to all the data in the mail's array, then give a bias to adjust the result (like a first opinion on the content of the mail). ReLU will then filter all the unnecessary data. Then, Linear will "regroup" the data, and the process will start a second time. After this process, Linear will do one last analysis, and the data will be compress into a number between 0 and 1, using Sigmoid. The model looks like this: 

Layer1:
    Linear
    ReLU
Layer2:
    Linear
    ReLU
Layer3:
    Linear
    Sigmoid

The treshold for Spam mail is at 0.8. If the score is lower, the mail won't be considered a Spam.

The model was tested on 1146 mails. Here are the results:

- Only 17 spams managed to get through the model (1.5%)
- Only 1 non spam mail ended up in the spams (0.08%)

## Getting Started

### Dependencies

fastapi              0.128.0
joblib               1.5.3
nltk                 3.9.2
numpy                2.4.1
pandas               3.0.0
pydantic             2.12.5
regex                2026.1.15
scikit-learn         1.8.0
toarray              0.3.2
torch                2.10.0
uvicorn              0.40.0

You can install all the modules using pip as below

`pip install [dependency]` or  `python -m pip install [dependency]`

### Download

You can download the program here: 

### Executing Program

To start the program you first need to activate a Virtual environment using this command:
`.\SpamDetector\Scripts\activate`

Then you need to go to the backend directory and start the server:
`cd backend`
`fastapi dev app.py`

## Author

Lucas Delvoy
@LucasDelvoy

## Version History



## Acknowledgment

Dataset found here: https://www.kaggle.com/datasets/jackksoncsie/spam-email-dataset/data