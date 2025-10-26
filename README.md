# AutomationExercise Robot Driver API

This project is a Python automation service that logs into [AutomationExercise](https://automationexercise.com), searches for a product, and returns product details via an API. You can use it to check if a specific product exists and get its details via a simple HTTP request.

---

## Features

- Log in to AutomationExercise using your credentials.  
- Search for a product on the website (partial match allowed).  
- Return product details if exactly one product is found.  
- Return a “product not found” message if no product or multiple matches are found.  
- Access the automation remotely through an API.  
- Console logs show the progress of the automation.

---

## Requirements

- Python 3.11 or higher  
- `pip` (Python package manager)  
- Playwright (for browser automation)  

---

## Setup Instructions

Follow these steps carefully:

### For running the task-03 including deployment

### 1. Clone the project  

```bash
git clone <your-repo-url>
cd <project-folder>

```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requiremetns.txt
playwright install

```

### 3. Running API
```bash
uvicorn main:app --reload
```

### 4. For checking if the api is running or not
- check this endpoint - http://127.0.0.1:8000/


### 5. Hit the POST request by passing the following parameters
- hit Post request on - http://127.0.0.1:8000/run-task
```bash
{
  "username": "nanlogx@gmail.com",
  "password": "Login@12345",
  "product": "shirt"
}
```


### Note:
- If you want run only the task-01 you can go "rb-1-roboto-driver" and run the code by using 
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requiremetns.txt
playwright install
pip install -r requiremetns.txt 
python main.py
```

- Couldn't finish the task-02 but its code can be found inside the "rb-2-ai-automation" branch.