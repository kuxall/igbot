import streamlit as st
import requests
from bs4 import BeautifulSoup
from instabot import Bot
import time
import os
import glob
import random

# Function to scrape Instagram profiles
def scrape_instagram_profiles(location):
    keyword_search_location = f"instagram smoke shop {location}"
    url = f"https://www.google.com/search?q={keyword_search_location}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    results = soup.select(".tF2Cxc")

    profiles = []
    for result in results:
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

# Function to send messages to Instagram users
def send_instagram_messages(profiles, message):
    cookie_path = "./config/*cookie.json"

# Check if the cookie file exists
    if glob.glob(cookie_path):
        # If it exists, delete it
        os.remove(glob.glob(cookie_path)[0])

    bot = Bot()
    bot.login(username="prdev00", password="sherpatesting")
    
    for profile in profiles:
        instagram_id = profile["Profile ID"]
        bot.send_message(message, [instagram_id])
        time.sleep(random.randint(1, 10))
    
    bot.logout()
# Streamlit app
def app():
    st.title("Instagram DM Sender")
    
    city_options = ["New York City", "Los Angeles", "Chicago", "Houston", "Miami", "San Francisco", "Seattle", "Washington", "Boston"]
    city = st.sidebar.selectbox("Select a city to scrape Instagram profiles for", city_options)
    
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
    
    if st.button("Send messages to Instagram users"):
        message = st.text_input("Enter your message")
        st.write("Sending messages...")
        send_instagram_messages(profiles, message)
        st.write("Messages sent!")


if __name__ =="__main__":
    app()