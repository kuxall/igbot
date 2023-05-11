# Import necessary libraries
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

# Function to scrape Instagram profiles
def scrape_instagram_profiles(location):
    # Create search query for Google search
    keyword_search_location = f"instagram smoke shop {location}"
    url = f"https://www.google.com/search?q={keyword_search_location}"

    # Set user agent header to avoid being blocked by Google
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # Send request to Google and extract profiles from search results
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.select(".tF2Cxc")

    profiles = []
    for result in results:
        # Extract profile information from search result
        title = result.select_one(".DKV0Md").text
        link = result.a["href"]
        if link.startswith("https://www.instagram.com/") and "/p/" not in link and "/explore/" not in link:
            profile_link = link.split("?")[0]  # Remove any query parameters from the link
            profile_id = profile_link.split("/")[-2]  # Extract the Instagram ID from the link
            profiles.append({
                "Title": title,
                "Profile Link": profile_link,
                "Profile ID": profile_id
            })
    
    return profiles


# Function to generate messages using OpenAI API
def create_message(prompt, profile_id):
    model_engine = "text-curie-001"
    message_prompt = f"create an Instagram message for a new vape product 'HQQ' to {profile_id}"
    openai.api_key = "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"
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
def send_instagram_message(profile_id, message):
    # Delete existing cookie file to avoid login errors
    cookie_path = "config/*cookie.json"
    if glob.glob(cookie_path):
        os.remove(glob.glob(cookie_path)[0])

    # Login to Instagram account and send message
    bot = Bot()
    bot.login(username="nepadevelopment", password="Password!123")
    bot.send_message(message, [profile_id])
    time.sleep(random.randint(1, 10))
    bot.logout()


# Main Streamlit application function
def app():
    st.title("Instagram DM Sender")

    # Load the list of cities from the CSV file
    cities = []
    with open('cities.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            city = row['City']
            cities.append(city)

    # Use the list of cities in the selectbox
    city = st.sidebar.selectbox("Select a city to scrape Instagram profiles for", cities)

    # Scrape Instagram profiles for the selected city
    st.write(f"Collecting Instagram profiles for {city}...")
    profiles = scrape_instagram_profiles(city)
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
            generated_message = create_message("create an Instagram message for a new vape product 'HQQ'", profile["Profile ID"])
            messages.append(generated_message)
            st.write(f"Generated message for {profile['Profile ID']}: {generated_message}")

        # Send messages to each profile
        st.write("Sending messages...")
        for i, profile in enumerate(profiles):
            send_instagram_message(profile["Profile ID"], messages[i])
            st.write(f"Sent message to {profile['Profile ID']}: {messages[i]}")
        st.write("Messages sent!")

if __name__ =="__main__":
    app()