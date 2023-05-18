import streamlit as st
import requests
from bs4 import BeautifulSoup
from instabot import Bot
import time
import os
import glob
import random
import openai
import csv
from dotenv import load_dotenv
from typing import Iterator

# Load environment variables from .env file
load_dotenv()

# Function to scrape Instagram profiles
def get_insta_accounts(location: str, num_pages: int = 5) -> Iterator[dict]:
    search_query = f'instagram smoke shop {location}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    for page in range(num_pages):
        start = page * 10
        url = f'https://www.google.com/search?q={search_query}&start={start}'

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        search_results = soup.find_all('div', {'class': 'g'})

        for result in search_results:
            if 'instagram.com' in result.find('a')['href']:
                profile_link = result.find('a')['href']
                profile_title = result.find('h3').text
                profile_id = profile_link.split('/')[3]
                yield {
                    'Title': profile_title,
                    'Profile Link': profile_link,
                    'Profile ID': profile_id
                }

# Function to generate messages using OpenAI API
def create_message(prompt, profile_id):
    model_engine = "text-curie-001"
    openai.api_key = os.environ['OPENAI_API_KEY']  # Access the environment variable
    message_prompt = f"create an Instagram message for a new vape product 'HVQ' to {profile_id}"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=message_prompt,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()

# Function to send messages to Instagram users
def send_instagram_message(profile_id, message, bot):
    # Delete existing cookie file to avoid login errors
    cookie_path = "config/*cookie.json"
    if glob.glob(cookie_path):
        os.remove(glob.glob(cookie_path)[0])
    bot.send_message(message, [profile_id])
    time.sleep(random.randint(1, 10))

# Main Streamlit application function
def app():
    st.title("Instagram DM Sender")

    # Load the list of cities from the CSV file
    cities = []
    with open('./data/cities.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            city = row['City']
            cities.append(city)

    # Create a list of Instagram accounts
    accounts = [
        {
            "username": os.getenv("INSTAGRAM_USERNAME_1"),
            "password": os.getenv("INSTAGRAM_PASSWORD_1")
        },
        {
            "username": os.getenv("INSTAGRAM_USERNAME_2"),
            "password": os.getenv("INSTAGRAM_PASSWORD_2")
        },
        # Add more accounts if needed
    ]

    # Loop through the list of cities and scrape Instagram profiles and send messages for each city
    for city in cities:
        # Scrape Instagram profiles for the selected city
        st.write(f"Collecting Instagram profiles for {city}...")
        profiles = list(get_insta_accounts(city))
        st.subheader(f"Found {len(profiles)} profiles!")

        if len(profiles) > 0:
            st.write("Scraped profiles:")
            for profile in profiles:
                st.write(f"Title: {profile['Title']}")
                st.write(f"Profile Link: {profile['Profile Link']}")
                st.write(f"Profile ID: {profile['Profile ID']}")
                st.write("---")

            # Generate messages for each profile using OpenAI API
            st.write("Generating messages...")
            messages = []
            for profile in profiles:
                generated_message = create_message("create an Instagram message for a new vape product 'HVQ'", profile["Profile ID"])
                messages.append(generated_message)
                st.write(f"Generated message for {profile['Profile ID']}: {generated_message}")

            # Send messages to each profile using different accounts
            st.write("Sending messages...")
            num_accounts = len(accounts)
            for i, profile in enumerate(profiles):
                account_index = i % num_accounts  # Determine the index of the Instagram account to use
                account = accounts[account_index]
                bot = Bot()
                bot.login(username=account["username"], password=account["password"])
                send_instagram_message(profile["Profile ID"], messages[i], bot)
                bot.logout()
                st.write(f"Sent message to {profile['Profile ID']} using {account['username']}: {messages[i]}")
            st.write("Messages sent!")

if __name__ == '__main__':
    app()
