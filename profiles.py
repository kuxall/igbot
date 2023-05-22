import streamlit as st
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse, parse_qs
import time


# Function to scrape Instagram profiles
def get_insta_accounts(location, num_pages=10):
    profiles = []

    for page in range(num_pages):
        # Create search query for Google search
        keyword_search_location = f"instagram smoke shop {location}"
        start = page * 10
        url = f"https://www.google.com/search?q={keyword_search_location}&start={start}"

        # Set user agent header to avoid being blocked by Google
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

        # Send request to Google and extract profiles from search results
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        div_elements = soup.select("div.egMi0.kCrYT")

        for div in div_elements:
            # Extract the profile link from the href attribute
            href = div.find("a")["href"]
            parsed_url = urlparse(href)
            query_params = parse_qs(parsed_url.query)
            profile_link = query_params.get("url", [""])[0]

            # Check if the profile link belongs to Instagram
            if (
                profile_link.startswith("https://www.instagram.com/")
                and "/p/" not in profile_link
                and "/explore/" not in profile_link
                and "?utm_medium=copy_link" not in profile_link
                and "?hl=ne" not in profile_link
            ):
                # Extract the profile ID from the link
                profile_id = profile_link.strip("/").split("/")[-1]

                # Extract the title from the h3 element
                title = div.select_one(
                    "div.DnJfK div.j039Wc h3 div.BNeawe.vvjwJb.AP7Wnd"
                ).text

                # Append the profile information to the list
                profiles.append(
                    {
                        "Title": title,
                        "Profile Link": profile_link,
                        "Profile ID": profile_id,
                    }
                )

    return profiles


# Main function to scrape profiles for selected city
def scrape_profiles_for_city(city):
    profiles = get_insta_accounts(city, num_pages=5)

    # Generate timestamp for the filename
    timestamp = time.strftime("%Y%m%d%H%M%S")

    # Save the profiles to a CSV file with the timestamp in the filename
    output_file = f"./profiles/{city}_profiles_{timestamp}.csv"
    with open(output_file, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=["Title", "Profile Link", "Profile ID"]
        )
        writer.writeheader()
        writer.writerows(profiles)

    return profiles


if __name__ == "__main__":
    # Load the list of cities from the CSV file
    cities = []

    with open("./data/cities.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            city = row["City"]
            cities.append(city)

    # Create a Streamlit app to select the city
    st.title("Instagram Profiles Scraper")
    selected_city = st.selectbox("Select a city:", cities)
    if st.button("Scrape Profiles"):
        profiles = scrape_profiles_for_city(selected_city)
        st.subheader(f"Found {len(profiles)} profiles!")

        if len(profiles) > 0:
            st.write("Scraped profiles:")
            for profile in profiles:
                st.write(f"Title: {profile['Title']}")
                st.write(f"Profile Link: {profile['Profile Link']}")
                st.write(f"Profile ID: {profile['Profile ID']}")
                st.write("---")
        else:
            st.write("No profiles found.")
        st.success(f"Scraped profiles for {selected_city}!")
