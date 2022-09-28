# Mapping city-wide perceptions of neighbourhood quality using street-view images: a methodological toolkit

## <p align=center> :camera: :city_sunset: :thought_balloon: :ok_woman: :sparkling_heart: :question: </p>

## Description

We provide all the necessary components to launch your own urban perceptions survey using street view images. This work is part of Emily Muller's PhD funded by the MRC Center for Environment & Health. 

## System Requirements

| Program                                                    | Version                  |
| ---------------------------------------------------------- | ------------------------ |
| [Python](https://www.python.org/downloads/)                | >= 3.7                   |
| [QGIS](https://qgis.org/en/site/)                          | >= 3.14.1-Pi           | 
| [GNU parallel](https://www.gnu.org/software/parallel/)     |  |
| [Postgresql](https://www.postgresql.org/)                  | >= 11.17                 |
| [Node.js](https://nodejs.org/en/)                          | >= 16.13.2                |
| [kubectl](https://kubernetes.io/docs/tasks/tools/)         | ==v1.20.2              |
| [wandb](https://wandb.ai/site)                              |              |

Python and npm modules are included in requirement.txt files.

## How to Use this Repository

This repository has 3 core components:

| Title                                            | Description                                                                                                                                                                                                     | Location                                   | Key Components Objectives                                                                                                                                                                                                                                                                                                           |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Introduction to Environmental Health and Imagery | This is a short video, introducing the domain, methods and describing some pioneering work in this field                                                                                                        | [Video](https://youtu.be/-b92eKqxS0A)                             | Introduction to the field. Understand different methods. Understand different types of data. Be aware of seminal research.                                                                                                                                                                                                        |
| `download_images`          | This repository contains all the code needed to download google street view images. | [download_images](docs/1.download_images.md) | Get all available images from Google Street View. Select images to download. |
| `web_app`          | This repository contains all the code needed to build a web-app to survey user pairwise image ratins. | [web_app](docs/2.web_app.md) | Build database, back-end and front-end. Dockerise and host using kubernetes. |
| `deep_cnn`                                       | This module contains all the code needed to fine-tune a deep neural network. | [deep_cnn](docs/3.deep_cnn.md)         | Use terminal for executing python scripts Train a PyTorch model and visualise results.  Implement bash script. Iterate on model hyperparameters to optimise model.   |

## Getting started

Clone this repository into your local drive.

```sh
git clone https://github.com/emilymuller1991/urban-perceptions.git
cd urban-perceptions
```

### Setting up a virtual environment

We will set up a virtual environment for running our scripts. In this case, installing specific package versions will not interfere with other programmes we run locally as the environment is contained. Initially, let's set up a virtual environment:

```sh
virtualenv --python=python3.7 venv
```

This will create a new folder for the virtual environment named venv` in your repository. We activate this environment by running

```sh
source venv/bin/activate
```

We install dependencies by running

```
pip install requirements.txt
```

Note this will only install python dependencies. We will also need other software utilies at various stages throughout this procotol.

### Setting up the development virtual environment

The `pytest` and pre-commit module is required for running tests and formatting. This can be installed by running:

```sh
pip install requirements_dev.txt
```

Now run the tests below to make sure everything is set up correctly. Then, proceed to the video.

### Testing

To run all tests, install `pytest`. After installing, run

```sh
pytest tests/ -v
```
