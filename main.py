import requests
import logging
import re
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://www.risto3.it/it/ristoranti/ristoranti-e-menu/trentino-sviluppo-rovereto/"
response = requests.get(url)
response.raise_for_status()  
soup = BeautifulSoup(response.text, 'html.parser')
menu_sections = soup.find_all('div', class_='daily-menu-category-container')

formatted_menu = ""

# Configurazione di logging per scrivere su un file
logging.basicConfig(filename='data.log',  # Specifica il nome del file
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')

primi_status = "not found"
secondi_status = "not found"
contorni_status = "not found"
for section in menu_sections:
    # Replace multiple spaces and new-lines with single ones
    section_text = re.sub(r'\n+', '\n', section.get_text(strip=False))
    section_text = re.sub(r'[^\S\n]+', ' ', section_text)
    # Do not process rows with prices
    if not "Euro" in section_text:
        if "Primi" in section_text:
            primi_status = "found"
        if "Secondi" in section_text:
            secondi_status = "found"
        if "Contorni" in section_text:
            contorni_status = "found"

        for line in section_text.splitlines():
            if line.strip() != "":
                formatted_menu = formatted_menu + line + "\n"
        formatted_menu = formatted_menu + "\n"


date_today = datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
filename = f"data/menu_{date_today}.txt"
with open(filename, "w") as file:
    file.write(f"Menu del giorno {date_today} \n\n")
    file.write(formatted_menu)

logging.info(f"Menu salvato in {filename}")
logging.info(f"Output status - primi: {primi_status}, secondi: {secondi_status} , contorni: {contorni_status}")