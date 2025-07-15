import requests
import os
import datetime
import time
import random


def get_quote():
    try:
        params = {
            'method': 'getQuote',
            'format': 'json',
            'lang': 'en'
        }

        for _ in range(3):
            try:

                response = requests.get("https://api.forismatic.com/api/1.0/", params=params)
                if response.status_code == 200:
                    data = response.json()
                    quote_text = data['quoteText'].strip()
                    quote_author = data['quoteAuthor'].strip() if data['quoteAuthor'] else "Unknown"
                    return f"{quote_text} - {quote_author}"
                print(f"API attempt failed with status code: {response.status_code}")
            except Exception as e:
                print(f"Request attempt error: {e}")
            time.sleep(2)
            

        fallback_quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Life is what happens when you're busy making other plans. - John Lennon",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "Simplicity is the ultimate sophistication. - Leonardo da Vinci",
            "It does not matter how slowly you go as long as you do not stop. - Confucius"
        ]
        print("Using fallback quote after API attempts failed")
        return random.choice(fallback_quotes)
    except Exception as e:
        print(f"Unexpected error in get_quote: {e}")
        return f"An error occurred: {e}"


def main():
    webhook_url = os.environ['DISCORD_WEBHOOK']
    today = datetime.datetime.now()
    today_formatted = today.strftime("%B %d %Y")
    
    quote = get_quote()
    

    if " - " in quote:
        quote_text, quote_author = quote.rsplit(" - ", 1)
    else:
        quote_text, quote_author = quote, "Unknown"
    

    embed = {
        "title": "🌟 Frase do Dia BECKA 🌟",
        "description": f"*\"{quote_text}\"*",
        "color": 15844367, 
        "author": {
            "name": quote_author
        },
        "footer": {
            "text": f"{today_formatted}"
        },
        "timestamp": today.isoformat()
    }
    
    message = {
        "embeds": [embed]
    }
    
    response = requests.post(webhook_url, json=message)
    
    if response.status_code in [200, 204]:
        print("Quote sent successfully.")
    else:
        print(f"Failed to send quote. Status code: {response.status_code}, Response: {response.text}")




if __name__ == "__main__":
    main()
