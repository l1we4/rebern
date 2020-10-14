from PIL import Image, ImageDraw, ImageFont
import json
import requests
import datetime
from io import BytesIO
import os

def current(rc, bg):
    responce_current = rc
    # Иконка
    icon = requests.get(f"https://openweathermap.org/img/wn/{responce_current['weather'][0]['icon']}@4x.png")
    icon = Image.open(BytesIO(icon.content))
    bg.paste(icon, (500,200), icon)

    #Рисование на БГ
    draw_text = ImageDraw.Draw(bg)

    #Шрифт
    font = ImageFont.truetype("./resource/Sitka.ttc", size=75)

    # Температура
    temp = f"{round(responce_current['main']['temp'])}c°"
    draw_text.text((530,450),temp ,font=font)

    # Город
    font = ImageFont.truetype("./resource/Sitka.ttc", size=55)
    city = responce_current['name']
    country = responce_current['sys']['country']

    w,h = draw_text.textsize(f'{city}/{country}')
    if w <= 43:
        W = (1050-w)/2
    else:
        W = (900-w)/2

    draw_text.text((W,120), f'{city}/{country}',font=font)
    return print("current End", h)


def one_call(ro, bg):
    responce_onecall = ro

    i = 1
    x = 165
    x1 = 185
    while True:
        if i != 6:
            # Запросы
            icon = responce_onecall['daily'][i]['weather'][0]['icon']
            tempDay = round(responce_onecall['daily'][i]['temp']['day'])
            tempNight = round(responce_onecall['daily'][i]['temp']['night'])
            date = datetime.datetime.utcfromtimestamp(responce_onecall['daily'][i]['dt']).strftime('%d.%m')
            
            #Шрифт
            font = ImageFont.truetype("./resource/Sitka.ttc", size=18)

            # Надписи на нижем док-баре
            draw_text = ImageDraw.Draw(bg)

            # Температура
            draw_text.text((x1, 715), f'{tempDay}/{tempNight}c°',font=font)
            
            # Дата
            draw_text.text((x1, 620), f'{date}', font = font)
           
            # Рисование иконки
            icon = requests.get(f"https://openweathermap.org/img/wn/{icon}@2x.png")
            icon = Image.open(BytesIO(icon.content))
            bg.paste(icon, (x, 630), icon)
            
            # Смешение координат
            x1 = x1 + 200
            x = x + 200
            i = i  + 1
        else:
            break

def doc_bar_left(rc, ro, bg, tran):
    responce_current = rc
    responce_onecall = ro

    #Текст док бара всех значений
    text_wind = tran['wind']
    text_humidity = tran['humidity'] 
    text_visibility = tran['visibility']
    text_pressure = tran['pressure']
    text_uvi = tran['uvi']
    text_suns = tran['suns']

    #Рисование на БГ
    draw_text = ImageDraw.Draw(bg)

    #Шрифт
    font = ImageFont.truetype("./resource/Sitka.ttc", size=30)
    
    #TimeZone
    timezone = responce_current['timezone']

    #Дата на сегодня
    date = datetime.datetime.utcfromtimestamp(responce_current['dt']+timezone).strftime('%d.%m')
    draw_text.text((80, 70), date, font=font)

    #Другой размер шрифта
    font_small = ImageFont.truetype("./resource/Sitka.ttc", size=25)

    #ветер
    wild = round(responce_current['wind']['speed'])
    text=  f'{text_wind}\n      {wild}m/s'
    draw_text.text((80, 120),text,font=font_small)
    
    #Влажность
    humidity = responce_current['main']['humidity']
    text = f'{text_humidity}\n     {humidity}%'
    draw_text.text((80,190), text, font= font_small)

    #Видимость
    visibility = responce_current['visibility']
    visibility = visibility / 1000
    text= f'{text_visibility}\n     {visibility}km'
    draw_text.text((80, 260),text ,font = font_small)

    #Давление
    pressure = responce_current['main']['pressure']
    text = f'{text_pressure}\n     {pressure}hPa'
    draw_text.text((80,330),text , font = font_small)

    #UV 
    uvi = round(responce_onecall['current']['uvi'])
    text = f'{text_uvi}\n     {uvi}'
    draw_text.text((80, 400), text, font = font_small)

    #Рассвет/закат
    sunrise = datetime.datetime.utcfromtimestamp(responce_current['sys']['sunrise'] + timezone).strftime('%H:%M')
    sunset =  datetime.datetime.utcfromtimestamp(responce_current['sys']['sunset'] + timezone).strftime('%H:%M')
    text = f'{text_suns}\n     {sunrise}, {sunset}'
    draw_text.text((80, 470),text ,font = font_small)

    return print("Left bar End")

def weather_start(city, responce_current, member_id, text):

    lat = responce_current['coord']['lat']
    lon = responce_current['coord']['lon']
    cheker = list(responce_current['weather'][0]['icon'])

    url_onecall = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&exclude=minutely,hourly&appid=bc6aa7041a41d2b23178b2828adba1ba"

    responce_onecall = (requests.get(url_onecall)).json()

    bg = Image.open(f"./resource/background/{cheker[2]}.png")
    frame = Image.open("./resource/frame.png")

    bg.paste(frame, (0,0), frame)
    current(responce_current, bg)
    one_call(responce_onecall, bg)
    doc_bar_left(responce_current, responce_onecall, bg, text)

    save_point= f"./resource/{member_id}.png"
    path = os.path.abspath(save_point)
    print(path)
    bg.save(save_point)
    return path
