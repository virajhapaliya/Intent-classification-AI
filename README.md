# Intent-classification-AI

- For this project use Python>=3.12

## Backend server

- Installation
  ```
  $ cd professors
  $ pip install -r requirements.
  ```
- Start server
  ```
  $ python manage.py runserver
  ```

## AI Server

- Installation
  ```
  $ cd AI
  $ pip install -r requirements.txt
  ```
- Run Script
  ```
  $ python intent_classification.py
  ```

## Instruction

- Start backend server first before starting AI application
- Currently for testing purpose sqlite3 is configured as database. From setting.py file we can change the configuration and use PosgreSQL
- Enter 'TOGETHER_API_KEY' in AI/.env file. You can api key from [Together AI](https://docs.together.ai/reference/chat-completions)
