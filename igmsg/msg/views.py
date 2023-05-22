from django.shortcuts import render
from .app import get_insta_accounts, create_message, send_instagram_message
from instabot import Bot
import csv
import environ


env = environ.Env()
environ.Env.read_env()

def scrape_instagram_profiles(request):
    # List of cities to scrape profiles from
    cities = []
    with open('D:/igbot/data/cities.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            city = row['City'].strip("'")
            cities.append(city)
            print(city)

    if request.method == 'POST':
        selected_city = request.POST.get('city')
        profiles = list(get_insta_accounts(selected_city))
        messages = []
        for profile in profiles:
            generated_message = create_message("create an Instagram message for a new vape product 'HVQ'", profile["Profile_ID"])
            messages.append(generated_message)
        return render(request, 'index.html', {'cities': cities, 'profiles': profiles, 'selected_city': selected_city})

    return render(request, 'index.html', {'cities': cities})

def send_messages(request):
    selected_city = request.POST.get('city')
    profiles = list(get_insta_accounts(selected_city))
    messages = []
    for profile in profiles:
        generated_message = create_message("create an Instagram message for a new vape product 'HVQ'", profile["Profile_ID"])
        messages.append(generated_message)
        bot = Bot()
        bot.login(username = env('username'), password = env('password'))
        for profile, message in zip(profiles, messages):
            send_instagram_message(profile["Profile_ID"], message, bot)
        bot.logout()
    return render(request, 'index.html', {'selected_city': selected_city, 'profiles': profiles, 'messages': messages})
