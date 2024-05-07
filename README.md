# IGBot

This is an Instagram Message Sender app.

This collects the instagram data from the google search and use those id's to send bulk messages to the respective targetted users.

#### Profile Scraper

- `profiles.py` collects the profiles from the every cities

```
streamlit run profiles.py
```
- `profiles/` stores the profiles information from every cities in this folder.

#### Message Sender

- `app.py` collects and sends the messages to the profiles collected.

```
streamlit run app.py
```
