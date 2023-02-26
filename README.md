# Prompt Experiment Management Example

## setup
```shell
cp .env.example .env
# Add your API key to the newly created .env file
poetry install
```

## run
```shell
poetry run python main.py +input=tech
# MULTIRUN
poetry run python main.py -m +input=tech,life
```
