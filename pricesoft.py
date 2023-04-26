import requests
import json
import re
import time
import random
import datetime

start_time = time.time()
items = [] # создаем переменную для списка айтемов
prices = [] # создаем переменную для списка цен с муна
percentage = []
good_items = []
c =(int(0))
sum_moon = (float(0))
sum_steam = (float(0))
final_perc = (float(0))
perc = int(input("Enter %: "))
delay = int(input("Enter delay between requests: "))
with open('items.txt', 'r+') as file:
    lines = file.readlines()
    file.seek(0)
    for line in lines:
        if line.strip():
            file.write(line)
    file.truncate()              
time.sleep(1)
for line in lines: # цикл прохода по строкам в текстовом файле
        if re.search('[a-zA-Z]', line): # если в строке нет знака доллара значит это название айтема
            items.append(line.strip()) # добавляем в список айтемов название айтема
        if '$' in line: # если в строке нет знака доллара значит это цена айтема
            price = line.strip().replace('$', '')  # убираем символ доллара из строки
            prices.append(float(price)) # добавляем цену айтема в список цен     
print('\nItems loaded: ',int(len(items)),'\nScan will start in 5 seconds ...\n')
time.sleep(5)
while len(items)>0: # цикл прохода по списку айтемов для получения цены айтема
    item_name = items[0] 
    market_hash_name = item_name.replace(" ", "%20")
    time.sleep(delay)
    response = requests.get('https://steamcommunity.com/market/priceoverview/?appid=252490&key=5E40EC4A717B88D2629CD4F237AD1ABE&market_hash_name={}&currency=1'.format(market_hash_name))
    data = response.json()
    if data != None and data !={'success': False}:
        price = data['lowest_price']
        price = float(price.replace('$', ''))
        c = c+1
        del items[0]
        if round(prices[0]/price*100,2)>perc: # если процент слива хороший 5
            print(item_name,'- GOOD' '\n', 'Steam price:', price, '\n Moon price:', prices[0], '\n',round(prices[0]/price*100,2),'%\n') # выводим цены с пометкой гуд
            good_items.append(item_name) # добавляем айтем в список хороших
            percentage.append(round(prices[0]/price*100,2))
            sum_moon = sum_moon + prices[0]
            sum_steam = sum_steam+price;
            del prices[0]
        else: # если процент слива плохой
            print(item_name, '\n', 'Steam price:', price, '\n Moon price:', prices[0], '\n',round(prices[0]/price*100,2),'%\n') # выводим цены
            del prices[0]
    else:        
        print('You got limit of requests, waiting 60 seconds ...\n')
        time.sleep(60)
    with open('result.txt', 'w') as file: # записываем в файл список хороших айтемов         
        for i in range(len(good_items)): # цикл прохода по списку хороших айтемов       
            file.write(good_items[i])
            file.write(' - ')
            file.write(str(percentage[i]))
            file.write('%\n')     
print('Checked',c,'items')
print('Good items:',len(good_items))
print('Bad items:',c-len(good_items))
final_perc = sum_moon/sum_steam
print('Rate is',round(final_perc*100,2),'%\n')
end_time = time.time()
total_time = end_time - start_time
total_time = int(total_time)
minutes, seconds = divmod(total_time, 60)
formatted_time = datetime.time(minute=minutes, second=seconds).strftime('%M minutes %S seconds')
print(f"Done for {formatted_time}")

        
    
        

        
    


    







