import requests
from datetime import datetime
from tkinter import *
from tkinter import messagebox
# Вся нужная для работы с Web-API информация:
api_key = 'd98dfb575279b28ae4c53301389d952d'  # уникальный ключ для подключения к погодному серверу
translator = {
    'Thunderstorm': 'Гроза',
    'Drizzle': 'Пасмурно, небольшие осадки',
    'Rain': 'Дождь',
    'Snow': 'Снег',
    'Mist': 'Туман',
    'Fog': 'Туман',
    'Clear': 'Ясно, без осадков',
    'Clouds': 'Пасмурно, без осадков',

}  # перевод погодных явлений на русский
weather_rate = {
    'Thunderstorm': 5,
    'Snow': 4,
    'Rain': 3,
    'Drizzle': 2,
    'Clouds': 1,
    'Clear': 0
}  # ранжирование погодных явлений по степени паршивости
icons = {
    'Thunderstorm': '11d',
    'Snow': '13d',
    'Rain': '10d',
    'Drizzle': '09d',
    'Clouds': '04d',
    'Clear': '01d'
}  # список иконок для пятидневного прогноза

# Вспомогательная функция получения и обработки прогноза погоды с сервера OpenWeatherMap
def get_weather(user_input):
    data_realtime = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=metric&APPID={api_key}&lang=ru")
    data = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={user_input}&units=metric&APPID={api_key}&lang=ru")
    if data:
        json_realtime = data_realtime.json()
        json = data.json()
        print(json_realtime,'\n',json)
        # (City, Country, temp_celsius, pressure, humidity, wind, icon, weather, current_time
        city = json['city']['name']
        country = json['city']['country']
        temp_celsius = json_realtime['main']['temp']
        pressure = json_realtime['main']['pressure'] / 1.33
        humidity = json_realtime['main']['humidity']
        wind = json_realtime['wind']['speed']
        icon = json_realtime['weather'][0]['icon']  # weather type is list
        weather = translator[json['list'][0]['weather'][0]['main']]
        current_time = datetime.fromtimestamp(json_realtime['dt'])  # время последнего изменения прогноза Weather
        # ОТСЮДА НАЧИНАЕТСЯ СЛОЖНАЯ ЧАСТЬ
        unique_dates = sorted(list({json['list'][i]['dt_txt'].split()[0] for i in range(40)}))
        weather_by_day = []
        for day in unique_dates:
            weather_by_day.append([])
            for element in json['list']:
                if element['dt_txt'].split()[0] == day:
                    weather_by_day[-1].append(element)
        print("mylist: {}".format(weather_by_day))
        forecast = []
        for day, elements_of_day in zip(unique_dates, weather_by_day):
            daydict = {"Day": day, }
            tmin = min([i['main']['temp_min'] for i in elements_of_day])
            tmax = max([i['main']['temp_max'] for i in elements_of_day])
            israin = 'Rain' in [i['weather'][0]['main'] for i in elements_of_day]
            try:
                worst_rate = max([weather_rate[i['weather'][0]['main']] for i in elements_of_day
                             if i['weather'][0]['main'] in weather_rate.keys()])
            except ValueError:
                worst_rate = 0
            worst = [list(item)[0] for item in weather_rate.items()
                     if list(item)[1] == worst_rate
            ][0]
            daydict["icon"] = icons[worst]
            daydict["t_min"] = tmin
            daydict["t_max"] = tmax
            daydict["is_rain"] = israin
            daydict['worst'] = worst
            forecast.append(daydict)
        print("forecast: {}".format(forecast))
        final = (city, country, temp_celsius, pressure, humidity, wind, icon, weather, current_time, forecast)
        return final
    else:
        return None

# Функция, которая получает на вход поисковый запрос, отправляет его на сервер, получает и обрабатывает
# прогноз с помощью функции search(), а затем обновляет данные на экране пользователя
def search():
    user_input = city_text.get()
    weather = get_weather(user_input)
    if weather:
        location_lbl['text'] = '{},{}'.format(weather[0], weather[1])
        icon['file'] = 'weather_icons/{}.png'.format(weather[6])
        temp_lbl['text'] = 'Температура: {:.2f}°C'.format(weather[2])
        weather_lbl['text'] = f'{weather[7]}'
        pressure_lbl['text'] = f'Давление: {round(weather[3])} мм. рт. ст.'
        humidity_lbl['text'] = f"Влажность: {weather[4]}%"
        wind_lbl['text'] = f'Ветер: {weather[5]} м/с'
        datetime_lbl['text'] = f'Последний прогноз: (UTC+3): {weather[8]}'
        fiveday_lbl['text'] = 'Прогноз погоды на 5 дней'
        f_day1['text'] = weather[9][0]['Day']
        f_day2['text'] = weather[9][1]['Day']
        f_day3['text'] = weather[9][2]['Day']
        f_day4['text'] = weather[9][3]['Day']
        f_day5['text'] = weather[9][4]['Day']
        f_icon1['file'] = 'weather_icons/{}.png'.format(weather[9][0]['icon'])
        f_icon2['file'] = 'weather_icons/{}.png'.format(weather[9][1]['icon'])
        f_icon3['file'] = 'weather_icons/{}.png'.format(weather[9][2]['icon'])
        f_icon4['file'] = 'weather_icons/{}.png'.format(weather[9][3]['icon'])
        f_icon5['file'] = 'weather_icons/{}.png'.format(weather[9][4]['icon'])
        f_tmin1['text'] = "{:.2f}°C".format(weather[9][0]['t_min'])
        f_tmin2['text'] = "{:.2f}°C".format(weather[9][1]['t_min'])
        f_tmin3['text'] = "{:.2f}°C".format(weather[9][2]['t_min'])
        f_tmin4['text'] = "{:.2f}°C".format(weather[9][3]['t_min'])
        f_tmin5['text'] = "{:.2f}°C".format(weather[9][4]['t_min'])
        f_tmax1['text'] = "{:.2f}°C".format(weather[9][0]['t_max'])
        f_tmax2['text'] = "{:.2f}°C".format(weather[9][1]['t_max'])
        f_tmax3['text'] = "{:.2f}°C".format(weather[9][2]['t_max'])
        f_tmax4['text'] = "{:.2f}°C".format(weather[9][3]['t_max'])
        f_tmax5['text'] = "{:.2f}°C".format(weather[9][4]['t_max'])
    else:
        messagebox.showerror('ERROR', 'Я не могу найти город с именем {}'.format(user_input))


# НАЧАЛО ФРОНТЕНД-ЧАСТИ - реализация интерфейса на TkInter
if __name__ == '__main__':
    # Создание обертки
    app = Tk()

    app.title("WEATHER FR🐸GCAST 1.001")
    app.geometry('600x700')
    app['background'] = '#856ff8'
    # Создание поля ввода, которое считывает текст введенный пользователем
    city_text = StringVar()
    city_entry = Entry(app, textvariable=city_text)
    city_entry.pack()
    # Создание кнопки поиска, которая при нажатии пользвователем на нее вызывает ф-ю search()
    search_btn = Button(app,text='Search Weather', width=20,command=search)
    search_btn.pack()
    #
    location_lbl = Label(app, text="",font=('bold',20),bg = "#856ff8")
    location_lbl.pack()
    #
    icon = PhotoImage(file = "")
    Icon = Label(app, image = icon, bg = "#856ff8")
    Icon.pack()
    #
    temp_lbl = Label(app, text="", bg = "#856ff8")
    temp_lbl.pack()
    #
    humidity_lbl = Label(app,text="", bg = "#856ff8")
    humidity_lbl.pack()
    #
    pressure_lbl = Label(app,text="", bg = "#856ff8")
    pressure_lbl.pack()
    #
    wind_lbl = Label(app,text="", bg = "#856ff8")
    wind_lbl.pack()
    #
    weather_lbl = Label(app, text="", bg = "#856ff8")
    weather_lbl.pack()
    #
    datetime_lbl = Label(app, text="", bg='#856ff8')
    datetime_lbl.pack()
    # Часть пятидневного прогноза
    fiveday_lbl = Label(app, text="", font=('bold',20), bg='#856ff8')
    fiveday_lbl.pack()
    frame = Frame(app, bg='#856ff8')
    frame1 = Frame(frame, bg='#856ff8')
    frame2 = Frame(frame, bg='#856ff8')
    frame3 = Frame(frame, bg='#856ff8')
    frame4 = Frame(frame, bg='#856ff8')
    frame5 = Frame(frame, bg='#856ff8')
    frame.pack()
    frame1.pack(side=LEFT)
    frame2.pack(side=LEFT)
    frame3.pack(side=LEFT)
    frame4.pack(side=LEFT)
    frame5.pack(side=LEFT)

    f_day1 = Label(frame1, text="", bg='#856ff8')
    f_day1.pack(side=TOP)
    f_day2 = Label(frame2, text="", bg='#856ff8')
    f_day2.pack(side=TOP)
    f_day3 = Label(frame3, text="", bg='#856ff8')
    f_day3.pack(side=TOP)
    f_day4 = Label(frame4, text="", bg='#856ff8')
    f_day4.pack(side=TOP)
    f_day5 = Label(frame5, text="", bg='#856ff8')
    f_day5.pack(side=TOP)

    f_icon1 = PhotoImage(file = "")
    Icon1 = Label(frame1, image = f_icon1, bg ="#856ff8")
    Icon1.pack(side=TOP)
    f_icon2 = PhotoImage(file = "")
    Icon2 = Label(frame2, image = f_icon2, bg ="#856ff8")
    Icon2.pack(side=TOP)
    f_icon3 = PhotoImage(file = "")
    Icon3 = Label(frame3, image = f_icon3, bg = "#856ff8")
    Icon3.pack(side=TOP)
    f_icon4 = PhotoImage(file = "")
    Icon4 = Label(frame4, image = f_icon4, bg = "#856ff8")
    Icon4.pack(side=TOP)
    f_icon5 = PhotoImage(file = "")
    Icon5 = Label(frame5, image = f_icon5, bg = "#856ff8")
    Icon5.pack(side=TOP)

    f_tmin1 = Label(frame1, text="", bg='#856ff8')
    f_tmin1.pack(side=BOTTOM)
    f_tmin2 = Label(frame2, text="", bg='#856ff8')
    f_tmin2.pack(side=BOTTOM)
    f_tmin3 = Label(frame3, text="", bg='#856ff8')
    f_tmin3.pack(side=BOTTOM)
    f_tmin4 = Label(frame4, text="", bg='#856ff8')
    f_tmin4.pack(side=BOTTOM)
    f_tmin5 = Label(frame5, text="", bg='#856ff8')
    f_tmin5.pack(side=BOTTOM)

    f_tmax1 = Label(frame1, text="", bg="#856ff8")
    f_tmax1.pack(side=BOTTOM)
    f_tmax2 = Label(frame2, text="", bg="#856ff8")
    f_tmax2.pack(side=BOTTOM)
    f_tmax3 = Label(frame3, text="", bg="#856ff8")
    f_tmax3.pack(side=BOTTOM)
    f_tmax4 = Label(frame4, text="", bg="#856ff8")
    f_tmax4.pack(side=BOTTOM)
    f_tmax5 = Label(frame5, text="", bg="#856ff8")
    f_tmax5.pack(side=BOTTOM)

    app.mainloop()
