## Environment Setup

How to familiar with the project ?

Run the following command before executing other commands

Don't change the execute path

1. clone the repository

    ```bash
    git clone https://github.com/Pleasurecruise/3D-AI-Agent.git --depth 1
    cd Linly-Talker
    git submodule update --init --recursive
    ```
2. create the `conda` environment

    ```bash
    conda create -n 3D-AI-Agent python=3.10
    conda activate 3D-AI-Agent
    pip install -r requirements.txt
    ````

## Usage

You can choose to use the local model or the online api to run the program.

1. use local model, click [here](README_local.md)

2. use online api, click [here](README_api.md)
