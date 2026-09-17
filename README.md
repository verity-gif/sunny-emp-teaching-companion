# Sunny — EMP Teaching Companion

Sunny is a Streamlit chatbot for practical EMP teaching support. It provides
written answers and optional AI-generated spoken replies using an original,
warm country-educator character.

Sunny is not Dolly Parton and does not imitate her identity or distinctive
voice. The app clearly tells users that its spoken voice is AI-generated.

## What the app includes

- API key held securely by the hosting service and never shown to visitors
- EMP level and task selection
- Chat history during the current browser session
- Original country-inspired writing personality
- Optional spoken responses and replay buttons
- A reminder not to enter identifiable student information
- Guardrails against inventing EMP-specific facts
- EMP orange and navy styling

## Run it on a Windows computer

### 1. Install Python

Install a current version of Python from <https://www.python.org/downloads/>.
During installation, tick **Add Python to PATH**.

### 2. Open the project in Visual Studio Code

Open the `sunny_emp_app` folder. Then choose **Terminal > New Terminal**.

### 3. Create a virtual environment

In the terminal, run:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt instead and run:

```bat
.venv\Scripts\activate.bat
```

### 4. Install the app requirements

```powershell
python -m pip install -r requirements.txt
```

### 5. Start the app

```powershell
python -m streamlit run app.py
```

Your browser should open automatically. If it does not, copy the local address
shown in the terminal, normally `http://localhost:8501`.

### 6. Use the app

For local testing, copy `.streamlit/secrets.toml.example` to
`.streamlit/secrets.toml`, then place the API key in that private file. Never
upload `secrets.toml` to GitHub.

1. Select the appropriate EMP level and type of support.
2. Choose whether replies should be spoken aloud.
3. Ask a teaching question in the message box.

An API key is separate from a ChatGPT subscription. API usage is billed through
the OpenAI API account associated with that key.

Each browser session is limited to 15 questions for the public training version.
The OpenAI account should also have a low project budget and usage alerts because
a session limit is not a substitute for an account-level spending limit.

## Important limitations

The first version knows the teaching approach described in its instructions,
but it does not contain the full EMP books or internal knowledge base. It is
specifically instructed not to invent lesson numbers, resource content, policy,
pricing or program claims. A future version can add approved EMP documents as a
controlled knowledge source.

Do not enter student names, contact details, dates of birth, health information
or other confidential information.

## Optional deployment

The app can later be deployed privately using Streamlit Community Cloud or an
EMP-controlled server. Before providing it to schools, add authentication,
central API-key management, usage limits, privacy terms, logging controls and a
curated EMP knowledge base.
