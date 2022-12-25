# symptom-checker
Telegram bot for diabetes and hypertension symptom checking built as a course project for Decision Support Systems in Medicine and Healthcare.  

## Functionality
This bot is able to ask patient questions about their symptoms and based on provided information it reponds with diagnosis and a set of recommendations.
  
## Scope
The scope is Diabetes and arterial hypertension.

## Usage
To start the bot you need to write your bot's token into `token` file and place that file into the repo's root folder.  
After that install the requirements:  
```bash
pip install -r requirements.txt
```

Finally, run the bot's app using:
```bash
python3 main.py
```

## Privacy
The bot stores the information about the user only in memory while the session runs and explicitly deletes it when user cancels the conversation or reaches the end of it.

## Limitations
- Supports concurrent users, but frees the user's record only on explicit end of conversation
- Provides diagnoses and recommendations based on the official Russian Ministry of Health guidelines, but the model is very simple - is not able to give precise diagnoses as a specialist
- Scope - only diabetes and hypertension are diagnosed
