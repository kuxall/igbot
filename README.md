# IGMSG

This is an Instagram Message Sender app.

This collects the instagram data from the google search and use those id's to send bulk messages to the respective targetted users.

Importing Required Libraries: This block imports the necessary libraries required for the application, including `Streamlit`, `requests`, `BeautifulSoup`, `instabot`, `time`, `os`, `glob`, `random`, `openai`, `csv`, and `dotenv`. These libraries are used for various functionalities like web scraping, Instagram messaging, API integration, and more.

Load Environment Variables: The `load_dotenv()` function is called to load environment variables from a .env file. Environment variables are used to store sensitive information like API keys and account credentials securely.

Scraping Instagram Profiles: The `get_insta_accounts()` function is defined, which takes a location and the number of pages to scrape as input. It scrapes Instagram profiles related to smoke shops in the specified location by performing a Google search and extracting relevant information from the search results using BeautifulSoup. It yields a dictionary containing profile details like title, profile link, and profile ID for each scraped profile.

Generating Messages using OpenAI API: The `create_message()` function is defined, which takes a prompt (in this case, it's fixed) and a profile ID as input. It uses the OpenAI API to generate a message for a new vape product using the specified profile ID. It sends the prompt and receives a response from the OpenAI model, which is then returned as the generated message.

Sending Messages to Instagram Users: The `send_instagram_message()` function is defined, which takes a profile ID, message, and the Instagram bot instance as input. It sends the provided message to the specified profile ID using the Instagram bot. It first deletes any existing cookie file to avoid login errors, then sends the message, and finally adds a random delay between 1 and 10 seconds to simulate human-like behavior.

Main Streamlit Application Function: The `app()` function is defined, which serves as the main Streamlit application. It creates a Streamlit web application titled "Instagram DM Sender". It loads a list of cities from a CSV file, and then iterates through each city to scrape Instagram profiles, generate messages, and send them.

Loading the List of Cities: The cities list is initialized, and the CSV file `'cities.csv'` is read using the csv module. Each city name is extracted from the CSV file and appended to the cities list.

Instagram Accounts: The accounts list is initialized, which contains dictionaries with Instagram account credentials. These credentials are stored as environment variables `(INSTAGRAM_USERNAME_1, INSTAGRAM_PASSWORD_1, INSTAGRAM_USERNAME_2, INSTAGRAM_PASSWORD_2, etc.)` and accessed using os.getenv().

Scraping Instagram Profiles and Sending Messages: The code inside the for loop iterates through each city in the cities list. It calls the `get_insta_accounts()` function to scrape Instagram profiles for the current city. It then displays the scraped profile details using Streamlit's `st.write()` function. Next, it generates messages for each profile using the `create_message()` function and displays the generated messages. Finally, it sends the messages to the corresponding profiles using the `send_instagram_message()` function, using different Instagram accounts for each message.

Running the Streamlit Application: The `if __name__ == '__main__':` block ensures that the `app()` function is only executed when the script is run directly (not imported as a module). It calls the `app()` function to run the Streamlit application.

### What's Happening?
#### Issues
- The same code on `app.py` was working fine(below is the picture):
![Working Images](https://github.com/sherpa-codes/igbot/blob/main/images/instagram.png?raw=true)


- But now having this issues:
![Issue Images](https://github.com/sherpa-codes/igbot/blob/main/images/issues.png?raw=true)
