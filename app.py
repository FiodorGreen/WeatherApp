import requests
from tkinter import *
from tkinter import messagebox
api_key = 'd98dfb575279b28ae4c53301389d952d'
mydict = {
    'Thunderstorm': 'Гроза',
    'Drizzle': 'Пасмурно, небольшие осадки',
    'Rain': 'Дождь',
    'Snow': 'Снег',
    'Mist': 'Туман',
    'Fog': 'Туман',
    'Clear': 'Ясно, без осадков',
    'Clouds': 'Пасмурно, без осадков',

}
def get_weather(user_input):
    data = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={user_input}&units=metric&APPID={api_key}&lang=ru")
    if data:
        json = data.json()
        print(json,'\n',json)
        # (City, Country, temp_celsius, pressure, humidity, wind, icon, weather, current_time
        city = json['city']['name']
        country = json['city']['country']
        temp_celsius = json['list'][0]['main']['temp']
        pressure = json['list'][0]['main']['pressure'] / 1.33
        humidity = json['list'][0]['main']['humidity']
        wind = json['list'][0]['wind']['speed']
        icon = json['list'][0]['weather'][0]['icon']  # weather type is list
        weather = mydict[json['list'][0]['weather'][0]['main']]
        current_time = json['list'][0]['dt_txt']  # время последнего изменения прогноза Forecast
        mylist = [[], [], [], []]
        for i in range(5):
            mylist[0].append(json['list'][8*i]['dt_txt'])
            mylist[1].append(json['list'][8*i]['main']['temp'])
            mylist[2].append(json['list'][8*i]['weather'][0]['main'])
            mylist[3].append(json['list'][8*i]['weather'][0]['icon'])
        print(mylist)
        final = (city, country, temp_celsius, pressure, humidity, wind, icon, weather,current_time)

        print(final)
        return final
    else:
        return None


def search():
    user_input = city_text.get()
    weather = get_weather(user_input)
    if weather:
        location_lbl['text'] = '{},{}'.format(weather[0], weather[1])
        image['file'] = 'weather_icons/{}.png'.format(weather[6])
        temp_lbl['text'] = 'Температура: {:.2f}°C'.format(weather[2])
        weather_lbl['text'] = f'{weather[7]}'
        pressure_lbl['text'] = f'Давление: {round(weather[3])} мм. рт. ст.'
        humidity_lbl['text'] = f"Влажность: {weather[4]}%"
        wind_lbl['text'] = f'Ветер: {weather[5]} м/с'
        datetime_lbl['text'] = f'Последний прогноз: (UTC+3): {weather[8]}'
    else:
        messagebox.showerror('ERROR','Я не могу найти город с именем {}'.format(user_input))


app = Tk()

app.title("ПОГОДНОЕ ПРИЛОЖЕНИЕ 🐸")
app.geometry('700x350')
app['background'] = '#856ff8'
city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

search_btn = Button(app,text='Search Weather', width=20,command=search)
search_btn.pack()

location_lbl = Label(app, text="",font=('bold',20),bg = "#856ff8")
location_lbl.pack()

image = PhotoImage(file= "")
Image = Label(app, image = image, bg = "#856ff8")
Image.pack()

temp_lbl = Label(app, text="", bg = "#856ff8")
temp_lbl.pack()

humidity_lbl = Label(app,text="", bg = "#856ff8")
humidity_lbl.pack()

pressure_lbl = Label(app,text="", bg = "#856ff8")
pressure_lbl.pack()

wind_lbl = Label(app,text="", bg = "#856ff8")
wind_lbl.pack()

weather_lbl = Label(app, text="", bg = "#856ff8")
weather_lbl.pack()

datetime_lbl = Label(app, text="", bg='#856ff8')
datetime_lbl.pack()

fiveday_lbl = Label(app, text="", bg='#856ff8')
fiveday_lbl.pack()

app.mainloop()
