import requests
import os
import datetime
import time 


def get_quote():
    try:
        params = {
            'method': 'getQuote',
            'format': 'json',
            'lang': 'en'
        }

        for _ in range(3):
            response = requests.post("https://api.forismatic.com/api/1.0", data=params)
            if response.status_code == 200:
                data = response.json()
                quote_text = data['quoteText'].strip()
                quote_author = data['quoteAuthor'].strip() if data['quoteAuthor'] else "Unknown"
                return f"{quote_text} - {quote_author}"
            time.sleep(2)
        return "Failed to retrieve quote after multiple attempts."
    except Exception as e:
        return f"An error occurred: {e}"


def main():
    webhook_url = os.environ['DISCORD_WEBHOOK']
    today = datetime.datetime.now().strftime("%B %d %Y")

    quote = get_quote()
    message = {
        'content': f"A frase do dia para {today} é :\n\n{quote}"
    }  
    response = requests.post(webhook_url, json=message)

    if response.status_code in [200, 204]:
        print("Quote sent successfully.")
    else:
        print(f"Failed to send quote. Status code: {response.status_code}, Response: {response.text}")



        
if __name__ == "__main__":
    main()
