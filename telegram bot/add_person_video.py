from telegram.ext import Updater, CommandHandler, InlineQueryHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
import requests
import re
import logging 
import cv2
from first_comand import *
from dialog import *
from network import *
from add_person_video import *
import threading
from telegram import Bot, File
from datetime import datetime, date, time
import os
from PIL import Image 

#кнопки
global admin_keyboard
admin_keyboard=[["Заполнить анкету"], ["Распознать человека"], ["Вывести изображение с камеры"], ["Запись видео"], ["Удалить пользователя"]]

global user_keyboard
user_keyboard=[["Заполнить анкету"]]


def save_video(update, context, e, object):
    '''Входные данные - видео с изображением лица, выходные данные - сохранённые в базу данных изображения, натренированная модель.'''
    
    info=Bot.get_file(self = context.bot, file_id=object) #получение информацию для скачивания объекта
    name = File.download(info) # скачивание объекта в папку проекта, результат функции - имя файла
    os.rename(name, "video/"+"2_"+name)
    name = "video/"+"2_"+name
    com = cv2.VideoCapture(name) #Имя файла можно передать остальным функциям для работы с файлом
    totalNumFrames=com.get(cv2.CAP_PROP_FRAME_COUNT) #количество изображений в видео
    face_detector = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')#загрузка классификатора лиц

    context.bot.send_message(chat_id=update.effective_chat.id, text="Ваше видео сохранено, начинаем его обработку") #отправка сообщения пользовалелю
    
    #номер id
    file_id=open("data/file_id.txt", "r")
    face_id=int(file_id.read())
    file_id.close()
    
    count = 0 #счетчик кадров с наличием лица
    i=0 #индекс кадра
    
    while(True):
        i+=1
        com.set(cv2.CAP_PROP_POS_FRAMES, i) #индекс кадра, который будет захвачен следующим
        ret, img = com.read() #считывание изображения
        if not ret:
            print("Нет изображения")        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #перевод изображения в черно-белый

        #функция поиска лиц, определяются области, где есть лица
        faces = face_detector.detectMultiScale(gray, 
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(20, 20))
    
        # Сохранение захваченных изображений в папку "dataset"
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1            
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
    
            
    
        k = cv2.waitKey(100) & 0xff # Нажать 'ESC' для выхода
        if k == 27:
            break
        elif count >= 30: # Остановить видео, когда сделано 30 или более снимков
             break
    
    
    cv2.destroyAllWindows()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Закончили обработку видео, начинается обработка изображения лица, полученного из видео.")
    

    # путь к базе данных изображений лиц
    path = 'dataset'
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()#распознаватель лиц
    
    
    # получение изображения
    def getImagesAndLabels(path):
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]    #создание списка путей к изображениям 
        faceSamples=[] #массив с лицами
        ids = [] #массив с ID
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath) 
            img_numpy = np.array(PIL_img,'uint8')#перевод в формат массива
            id = int(os.path.split(imagePath)[-1].split(".")[1])#извлекается id человека на фото
            faces = face_detector.detectMultiScale(img_numpy)#определяет область, где есть человеческие лица, и возвращает список [x,y,w,h] с параметрами для каждого лица
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
        return faceSamples,ids
    
    print ("Происходит тренировка лиц")
    faces,ids = getImagesAndLabels(path) #принимает изображения из dataset и возвращает массивы лица и id
    recognizer.train(faces, np.array(ids))#тренируются данные
    
   
    recognizer.write('trainer/trainer.yml') # сохранение модели в trainer/trainer.yml
    
    
    print("Лицо натренировано. Выход из программы")#вывести номер натренированного лица и "завершение программы"
    context.bot.send_message(chat_id=update.effective_chat.id, text="Обработка изображения закончилась.")

    info=admin(update, context)
    if info=="a":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Вы зарегистрировались в системе! Можете воспользоваться доступными функциями.",  reply_markup=ReplyKeyboardMarkup(admin_keyboard, one_time_keyboard=True))
    if info=="p":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Вы зарегистрировались в системе!",  reply_markup=ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True))