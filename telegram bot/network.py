
import cv2
import numpy as np
import os 
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
import requests
import re
import logging 
from first_comand import *
from dialog import *
from datetime import datetime, date, time

#кнопки
global admin_keyboard
admin_keyboard=[["Заполнить анкету"], ["Распознать человека"], ["Вывести изображение с камеры"], ["Запись видео"], ["Удалить пользователя"]]

global stop_video_keyboard
stop_video_keyboard=[["Оcтановить запись видео"]]

global user_keyboard
user_keyboard=[["Заполнить анкету"]]

def open_cv(update, context, e_camera):
    '''Результат функции - определены: область с наличием лица, имя человека'''

    info=admin(update,context) #проверка, к какой группе относится пользователь

    if info=="unknown":
        context.bot.send_message(chat_id=update.effective_chat.id, text="У Вас ещё нет прав администратора, для их получения нажмите кнопку Начало работы и введите пароль администратора.", reply_markup=ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True))
    if info=="p":
        context.bot.send_message(chat_id=update.effective_chat.id, text="У Вас нет прав администратора. Вы можете только заполнить анкету", reply_markup=ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True))

    if info=="a":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ожидайте")
     
        recognizer = cv2.face.LBPHFaceRecognizer_create() #создание распознавателя лиц
        recognizer.read('trainer/trainer.yml') #получение натренированной модели
        cascadePath = "Cascades/haarcascade_frontalface_default.xml" #путь к класификатору лиц
        faceCascade = cv2.CascadeClassifier(cascadePath); #загрузка классификатора лиц
        
        
        font = cv2.FONT_HERSHEY_SIMPLEX #шрифт
        
        id = 0 #счетчик ID
        
        # Имена, связанные с ID
        names=[]
        information=open("data/name.txt", "r")
        for line in information:
            if line[-1]=="\n":
                line=line[:-1]
            names.append(line)
        print(names)
        information.close()
        
        # Начать захват видео с камеры
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) #установка ширины видео
        cam.set(4, 480) #установка высоты видео
        
        # Определение минимального размера окна для распознавания лица
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)
        

        while True:
            e_camera.wait()
            cam = cv2.VideoCapture(0) #захват видео
            ret, img =cam.read() #получение кадра
            if not ret:
                e_camera.clear()
                e_camera.wait()
                cam = cv2.VideoCapture(0) #захват видео
                ret, img =cam.read() #получение кадра
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  #перевод изображения в черно-белый
            
            
            #функция поиска лиц, определяются области, где есть лица
            faces = faceCascade.detectMultiScale(gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
               )

            test=0

            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                id, confidence = recognizer.predict(gray[y:y+h,x:x+w]) #получение id и отклонения
        
                # Проверка уверенности (0-идеальное совпадение), отправка пользователю фото и  имени 
                if confidence < 100:
                    name = names[id] 
                    confidence = "  {0}%".format(round(100 - confidence))
                    cv2.imwrite('image/photo.png', img)
                    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("image/photo.png", "rb") )
                    context.bot.send_message(chat_id=update.effective_chat.id, text=name, reply_markup=ReplyKeyboardMarkup(admin_keyboard, one_time_keyboard=True))
                    test=1

                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
                    print ("Лицо человека не распознано")
                    
                
            #если лицо распознано, остановить выполнение программы    
            if test:
                    break              
        
            k = cv2.waitKey(10) & 0xff # Начать 'ESC' для выхода из видео
            if k == 27:
                break
        
        # очистка камеры
        print("Выход из программы и очистка материала")
        cam.release()
        cv2.destroyAllWindows()

def get_video_file(update,context, e6, e_camera):
    '''Результат функции - видео с выделенной областью распознанного лица, именем человека и % совпадения'''
    
    info=admin(update,context) #проверка, к какой группе относится пользователь
    if info=="unknown":
        context.bot.send_message(chat_id=update.effective_chat.id, text="У Вас ещё нет прав администратора, для их получения нажмите кнопку Начало работы и введите пароль администратора.", reply_markup=ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True))
    if info=="p":
        context.bot.send_message(chat_id=update.effective_chat.id, text="У Вас нет прав администратора. Вы можете только заполнить анкету", reply_markup=ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True)) 
    
    if info=="a":         
        net=cv2.dnn.readNet("MobileNetSSD/MobileNetSSD_deploy.prototxt", "MobileNetSSD/MobileNetSSD_deploy.caffemodel") #чтение предварительно обученной модели и конфинурационного файла для распознавания образа человека
        recognizer = cv2.face.LBPHFaceRecognizer_create() #распознавател лиц
        recognizer.read('trainer/trainer.yml')#получение натренированной модели
        cascadePath = "Cascades/haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath);#классификатор лиц
        PERSON_CLASS_ID=15 #класс образа человека
        
        font = cv2.FONT_HERSHEY_SIMPLEX #шрифт        
        
        id = 0 #счетчик ID
        
        # Имена, связанные с ID
        names=[]
        information=open("data/name.txt", "r")
        for line in information:
            if line[-1]=="\n":
                line=line[:-1]
            names.append(line)
        print(names)
        information.close()
        
        cam = cv2.VideoCapture(0) #захват видео
        fourcc = cv2.VideoWriter_fourcc(*'XVID') #передает индификатор кодека, которым будем кодировать видео
        
        #запись в название видео даты и времени, в которое началась запись видео
        file_name = "video/"
        file_name += str(datetime.now())
        file_name=file_name.replace(".", " ")
        file_name=file_name.replace(":", "-")
        file_name+=".avi"
        print(file_name)

        video = cv2.VideoWriter(file_name, fourcc, 20.0, (640,480)) #создается объект, в который будет записываться видео кадр за кадром
        
        cam.set(3, 640) # установка ширины видео
        cam.set(4, 480) # установка высоты видео
        
        # Определение минимального размера окна для распознавания лица
        minW = 0.1*cam.get(3) 
        minH = 0.1*cam.get(4)

        i=0 #номер сделанного снимка
        ids=open("data/admins.txt", "r")
        for num, line in enumerate(ids, 0):
            if len(line)>1:
                id_chat=line
                id_chat=line
                context.bot.send_message(chat_id=id_chat, text="Началась запись видео")
                context.bot.send_message(chat_id=id_chat, text="Для остановки видео нажмите кнопку", reply_markup=ReplyKeyboardMarkup(stop_video_keyboard, one_time_keyboard=True))
        ids.close()

        while True:            
            e_camera.wait()
            cam = cv2.VideoCapture(0)
            ret, img =cam.read() 
            if not ret:
                e_camera.clear()
                e_camera.wait()
                cam = cv2.VideoCapture(0)
                ret, img =cam.read()

            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #изображение перводится в чёрно-белый
            blob=cv2.dnn.blobFromImage(img, scalefactor=1.0/127.5, size=(300, 300), mean=(127.5, 127.5, 127.5)) #возвращается массив  изображения
            net.setInput(blob) #передача массива в сеть
            out=net.forward()#результат
            for detection in out.reshape(-1, 7):
                conf=detection[2]
                classId=detection[1]
                if conf>0.5 and classId==PERSON_CLASS_ID: #проверка, есть ли на снимке человек                    
            
                    faces = faceCascade.detectMultiScale( #функция поиска лиц, определяются области, где есть лица
                        gray,
                        scaleFactor = 1.2,
                        minNeighbors = 5,
                        minSize = (int(minW), int(minH)),
                       )
           
                    for(x,y,w,h) in faces:
                        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])#recognizer.predict возвращает id и отклонение
                        print ("id ="+str(id))                        
        
                        # Проверка уверенности (0-идеальное совпадение) 
                        if (confidence < 100):
                            id = names[id]
                            confidence = "  {0}%".format(round(100 - confidence))
                            cv2.imwrite('image/photo.png', img)
                            print (id)
                        else:
                            id = "unknown"
                            confidence = "  {0}%".format(round(100 - confidence))
                    
                        
                        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)  #наложение на изображение имени человека
                        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1) #наложение на изображение %  совпадения
                      
                    video.write(img) #добавление кадра в видео
                    i+=1 #увеличение количества сделанных кадров
                    print(i)
                    
        
            if e6.is_set(): #остановка записи видео
               break
        
        video.release() #закрыть запить и сохранить все в файл    
        # очистка камеры
        print("Выход из программы и очистка материала")
        cam.release()
        cv2.destroyAllWindows()
        ids=open("data/admins.txt", "r")
        
        #отправка сообщения всем админимстраторам
        for num, line in enumerate(ids, 0):
            if len(line)>1:
                id_chat=line
                context.bot.send_message(chat_id=id_chat, text="Запись видео закончилась.", reply_markup=ReplyKeyboardMarkup(admin_keyboard, one_time_keyboard=True))
                com = cv2.VideoCapture(file_name) 
                totalNumFrames=com.get(cv2.CAP_PROP_FRAME_COUNT) # определение количества кадров в видео
                print (totalNumFrames)
                if totalNumFrames<=4500:
                    context.bot.send_video(chat_id=id_chat, video=open(file_name, "rb"))  #отправление получившегося видео пользователю
                else:
                    context.bot.send_message(chat_id=id_chat, text="Видео слишком большое. Вы можете посмотреть его на сервере.", reply_markup=ReplyKeyboardMarkup(admin_keyboard, one_time_keyboard=True))