import requests
from bs4 import BeautifulSoup
import pandas as pd

prices = []
locations = []
rooms = []
squares = []
floors = []

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.141 Mobile Safari/537.36"
}

urls = [
        'https://bina.az/baki/alqi-satqi/menziller/yeni-tikili?has_bill_of_sale=true&has_mortgage=true&has_repair=true&page=',
        'https://bina.az/baki/alqi-satqi/menziller/yeni-tikili?has_bill_of_sale=false&has_mortgage=true&has_repair=true&page=',
        'https://bina.az/baki/alqi-satqi/menziller/yeni-tikili?has_bill_of_sale=false&has_mortgage=false&has_repair=true&page=',
        'https://bina.az/baki/alqi-satqi/menziller/yeni-tikili?has_bill_of_sale=true&has_mortgage=false&has_repair=true&page=',
        'https://bina.az/baki/alqi-satqi/menziller/yeni-tikili?has_bill_of_sale=true&has_mortgage=true&has_repair=false&page=',
        'https://bina.az/baki/alqi-satqi/menziller/yeni-tikili?has_bill_of_sale=false&has_mortgage=true&has_repair=false&page=',
        'https://bina.az/baki/alqi-satqi/menziller/yeni-tikili?has_bill_of_sale=false&has_mortgage=false&has_repair=false&page=',
        'https://bina.az/baki/alqi-satqi/menziller/yeni-tikili?has_bill_of_sale=true&has_mortgage=false&has_repair=false&page=',
        'https://bina.az/baki/alqi-satqi/menziller/kohne-tikili?has_bill_of_sale=true&has_mortgage=true&has_repair=true&page=',
        'https://bina.az/baki/alqi-satqi/menziller/kohne-tikili?has_bill_of_sale=false&has_mortgage=true&has_repair=true&page=',
        'https://bina.az/baki/alqi-satqi/menziller/kohne-tikili?has_bill_of_sale=false&has_mortgage=false&has_repair=true&page=',
        'https://bina.az/baki/alqi-satqi/menziller/kohne-tikili?has_bill_of_sale=true&has_mortgage=false&has_repair=true&page=',
        'https://bina.az/baki/alqi-satqi/menziller/kohne-tikili?has_bill_of_sale=true&has_mortgage=true&has_repair=false&page=',
        'https://bina.az/baki/alqi-satqi/menziller/kohne-tikili?has_bill_of_sale=false&has_mortgage=true&has_repair=false&page=',
        'https://bina.az/baki/alqi-satqi/menziller/kohne-tikili?has_bill_of_sale=false&has_mortgage=false&has_repair=false&page=',
        'https://bina.az/baki/alqi-satqi/menziller/kohne-tikili?has_bill_of_sale=true&has_mortgage=false&has_repair=false&page=',
        ]

new_building = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]  #0 old building, 1 new building
has_repair = [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]  # 0 without repair, 1 with repair
has_bill_of_sale = [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1] # 0 no bill of sale, 1 has bill of sale
has_mortgage = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0] # 0 no mortgage, 1 has mortgage

csv_name = [
            "ApartmentNewRepairedHasBillHasMortgage.csv",
            "ApartmentNewRepairedNoBillHasMortgage.csv",
            "ApartmentNewRepairedNoBillNoMortgage.csv",
            "ApartmentNewRepairedHasBillNoMortgage.csv",
            "ApartmentNewNotRepairedHasBillHasMortgage.csv",
            "ApartmentNewNotRepairedNoBillHasMortgage.csv",
            "ApartmentNewNotRepairedNoBillNoMortgage.csv",
            "ApartmentNewNotRepairedHasBillHoMortgage.csv",
            "ApartmentOldRepairedHasBillHasMortgage.csv",
            "ApartmentOldRepairedNoBillHasMortgage.csv",
            "ApartmentOldRepairedNoBillNoMortgage.csv",
            "ApartmentOldRepairedHasBillNoMortgage.csv",
            "ApartmentOldNotRepairedHasBillHasMortgage.csv",
            "ApartmentOldNotRepairedNoBillHasMortgage.csv",
            "ApartmentOldNotRepairedNoBillNoMortgage.csv",
            "ApartmentOldNotRepairedHasBillHoMortgage.csv",
            ]

BakuApartmentData = pd.DataFrame()

for i in range(0, 16):
    page = 1
    print('Start of    ' + urls[i] + '    scaning')
    while True:
        print(str(page) + ' page scanned')
        url, page = urls[i] + str(page), page + 1
        req = requests.get(url, headers)

        html_page = req.text

        if "items items--no-results" in html_page:
            break

        soup = BeautifulSoup(html_page, "lxml")
        all_adds_href = soup.select("div[class=items_list]")
        price = all_adds_href[0].find_all(class_="price-val")
        location = all_adds_href[0].find_all(class_="location")
        name = all_adds_href[0].find_all(class_="name")

        for item in price:
            price_number = item.text.replace(" ", "")
            prices.append(int(price_number))

        for item in location:
            locations.append(item.text)

        for item in name:
            name = item.find_all("li")
            rooms_number = name[0].text.split()[0]
            square_number = name[1].text.split()[0]
            rooms.append(int(rooms_number))
            squares.append(float(square_number))
            try:
                floor_number = name[2].text.split()[0]
                floors.append(floor_number)
            except IndexError:
                floors.append(0)
                print('Append 0 to list')

    df = pd.DataFrame({
            "price": prices,
            "location": locations,
            "rooms": rooms,
            "square": squares,
            "floor": floors,
            'new_building': new_building[i],
            'has_repair': has_repair[i],
            'has_bill_of_sale': has_bill_of_sale[i],
            'has_mortgage': has_mortgage[i]
            })

df.to_csv('BakuApartmentData')
