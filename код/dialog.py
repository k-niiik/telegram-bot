from telegram.ext import Updater, CommandHandler, InlineQueryHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
import requests
import re
import logging 
import cv2
from add_person_video import *
from datetime import datetime, date, time
name=""
phone=""
apart=""
vozrast=""
info=""
id=0
video=""

#кнопки
global start_keyboard
start_keyboard=[["Начало работы"]]

global admin_keyboard
admin_keyboard=[["Заполнить анкету"], ["Распознать человека"], ["Вывести изображение с камеры"], ["Запись видео"], ["Удалить пользователя"]]

global user_keyboard
user_keyboard=[["Заполнить анкету"]]

global choice_keyboard
choice_keyboard=[["Верно"], ["Неверно"]]

def anketa_start(update, context,):  
    global inf
    inf=admin(update,context)
    if inf=="a" or inf=="p":

        #определение id будущего пользователя
        global id
        file_id=open("file_id.txt", "r")
        id=int(file_id.read())+1
        file_id.close()  
        
        context.bot.send_message(chat_id=update.effective_chat.id, text="Введите Ваше имя на русском или английском языке. Имя будет храниться в базе данных и в дальнейшем использоваться на английском языке.")
        return "get_name"
    if info=="unknown":
        context.bot.send_message(chat_id=update.effective_chat.id, text="У Вас ещё нет прав администратора, для их получения нажмите кнопку Начало работы и введите пароль администратора.", reply_markup=ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True))
def get_name(update, context):
    '''Получение имени пользователя, возвращается метка для перехода в функцию для получения видео'''
    global name
    name=update.message.text
    cyrillic = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    latin = 'a|b|v|g|d|e|e|zh|z|i|i|k|l|m|n|o|p|r|s|t|u|f|kh|tc|ch|sh|shch||y||e|iu|ia'.split('|')
    trantab = {k:v for k,v in zip(cyrillic,latin)}
    newtext = ''
    for ch in name:
        casefunc =  str.capitalize if ch.isupper() else str.lower
        newtext += casefunc(trantab.get(ch.lower(),ch))
    print(newtext)
    name=newtext
    context.bot.send_message(chat_id=update.effective_chat.id, text="Отправьте видео с изображением лица длиною 2-3 секунды (малый размер). Проверка видео может занять некоторое время.")
    return "get_video"
def get_video(update, context):
    '''Получение и проверка видео, возвращается метка для перехода в функцию для получения номера телефона'''
    face_detector = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')#загрузка классификатора лиц
    global video
    video=update.message.video    
    info=Bot.get_file(self = context.bot, file_id=video) #Получает информацию для скачивания объекта
    name = File.download(info) # Скачивает объект в папку проекта, результат функции - имя файла
    com = cv2.VideoCapture(name)
    totalNumFrames=com.get(cv2.CAP_PROP_FRAME_COUNT) #количество изображений
    count = 0
    i=0
    
    while i<totalNumFrames-1 and count<30:
        i+=1
        com.set(cv2.CAP_PROP_POS_FRAMES, i) #индекс кадра, который будет захвачен следующим
        ret, img = com.read()
        if not ret:
            print("Нет изображения")
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray,     #функция поиска лиц, определяются области, где есть лица
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(20, 20))
    
        for (x,y,w,h) in faces:
            
            count += 1
    if count>=30:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Введите номер телефона.")
        return "number"
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Не получилось распознать лицо. Отправьте видео с изображением лица длиною 2-3 секунды (малый размер). Проверка видео может занять некоторое время.")
        return "get_video"       
def number(update, context):
    '''Получение номера телефона, возвращается метка для перехода в  функцию для получения возраста'''
    global phone
    phone=update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text="Введите Ваш возраст")
    return "age"
def age(update, context):
    '''Получение возраста, возвращается метка для перехода в  функцию для проверки запелненных данных'''
    global vozrast
    global name
    global phone
    global info
    vozrast=update.message.text
    
    context.bot.send_message(chat_id=update.effective_chat.id, text="Результаты анкеты: Ваше ФИО {}, \n Ваш номер телефона {}, \n Ваш возраст {}".format(name, phone, vozrast), reply_markup=ReplyKeyboardMarkup(choice_keyboard, one_time_keyboard=True))
    info="Номер телефона: "+phone+". Возраст: "+vozrast+"\n"
    return "get_choice"
def get_choice(update, context):
    '''Получение выбора, правильно или нет заполнены данные'''
    choice=update.message.text
    if choice=="Неверно":
        anketa_start(update, context) #заполнить анкету заново
    elif choice=="Верно":
        #обработка видео
        global video        
        e=threading.Event()
        t = threading.Thread(target=save_video, args=(update, context, e, video))
        t.start() 
        
        if inf=="a":
            context.bot.send_message(chat_id=update.effective_chat.id, text="Вы заполнили данные анкеты! Начинаем работу с видео.", reply_markup=ReplyKeyboardMarkup(admin_keyboard, one_time_keyboard=True))
            true()
        if inf=="p":
            context.bot.send_message(chat_id=update.effective_chat.id, text="Вы заполнили данные анкеты! Начинаем работу с видео.", reply_markup=ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True))
            true()
def true ():
     global info
     global name

     #запись информации о пользователе в текстовый файл  
     information=open("info.txt", "a")
     information.write(info)
     information.close()

     #запись имени пользователя в текстовый файл
     information=open("name.txt", "a")
     information.write(name)
     information.write("\n")
     information.close()

     #запись нового последнего номера id
     file_id=open("file_id.txt", "w+")
     file_id.write(str(id))
     file_id.close()

     

def delete_person(update, context):
    info=admin(update,context)
    if info=="a":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Введите имя человека, которого вы хотите удалить")    
        return "person_name"
    if info=="unknown":
        context.bot.send_message(chat_id=update.effective_chat.id, text="У Вас ещё нет прав администратора, для их получения нажмите кнопку Начало работы и введите пароль администратора.", reply_markup=ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True))
    if info=="p":
        context.bot.send_message(chat_id=update.effective_chat.id, text="У Вас нет прав администратора.")
def person_name(update, context): 
    '''Получает имя пользователя, которого надо удалить и удаляет всю информацию о нём.'''
    name=update.message.text

    #перевод имени на английский
    cyrillic = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    latin = 'a|b|v|g|d|e|e|zh|z|i|i|k|l|m|n|o|p|r|s|t|u|f|kh|tc|ch|sh|shch||y||e|iu|ia'.split('|')
    trantab = {k:v for k,v in zip(cyrillic,latin)}
    newtext = ''
    for ch in name:
        casefunc =  str.capitalize if ch.isupper() else str.lower
        newtext += casefunc(trantab.get(ch.lower(),ch))
    print(newtext)
    name=newtext
    context.bot.send_message(chat_id=update.effective_chat.id, text="Имя записано")

    info=open("name.txt", "r")    
    person_information=""
    deleted_id=0

    #Id удаленного пользователя
    for num, line in enumerate(info, 0):
            if name in line:
                print(num)
                deleted_id=num
    info.close()
    if deleted_id!=0:      

    #Удаление другой информации о пользователе
            #Определение строки, которую надо удалить
        info=open("info.txt", "r")
        for num, line in enumerate(info, 1):
            if num==deleted_id:
                deleted_line=line
                print(deleted_line)
        info.close()
            #Создание нового списка информации
        info=open("info.txt", "r")
        for information in info:
            if information!=deleted_line and information!=deleted_line+"\n":            
                person_information+=information 
                print(person_information)
        info.close() 

            #Запись информации заново
        info=open("info.txt", "w+")
        info.write(person_information)
        info.close()     
        

        #новый список имен
        info=open("name.txt", "r")
        inf=""
        for name_person in info:
            print("да")
            if name_person!=name and name_person!=name+"\n":            
                inf+=name_person 
                print(inf)
        info.close()    
        
        #записать имена заново (без удаленного)
        info=open("name.txt", "w+")
        info.write(inf)
        info.close()  
        print("Файл с именами перезаписан")
        
        #поменять номер последнего id в файле
        ids=open("file_id.txt", "r")
        last_id=int(ids.read())
        id=last_id-1
        ids.close
        ids=open("file_id.txt", "w+")
        ids.write(str(id))
        ids.close()
        print("Id в файле изменено")
        
        #Удаление фото пользователя
        count=0    
        while count<30:
            count+=1       
            photo_name=""
            photo_name=photo_name+r"\User."+str(deleted_id)+"."+str(count)+".jpg"
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "dataset")
            path+=photo_name
            print(path)
            print("фото удалено")
            os.remove(path)
        
        #поменять номера id
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "dataset")
        deleted_id+=1
        while deleted_id<=last_id:
                count=0 
                while count<30:
                    count+=1  
                    file_name=path+r"\User."+str(deleted_id)+"."+str(count)+".jpg"
                    real_name=path+r"\User."+str(deleted_id-1)+"."+str(count)+".jpg"
                    os.rename(file_name, real_name)
                deleted_id+=1
        context.bot.send_message(chat_id=update.effective_chat.id, text="Пользователь удален", reply_markup=ReplyKeyboardMarkup(admin_keyboard, one_time_keyboard=True))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Пользователя с таким именем нет в базе данных.", reply_markup=ReplyKeyboardMarkup(admin_keyboard, one_time_keyboard=True))