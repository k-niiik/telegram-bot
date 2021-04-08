from telegram.ext import Updater, CommandHandler, InlineQueryHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
import requests
import re
import logging 
import cv2
from datetime import datetime, date, time
import time

#кнопки
global start_keyboard
start_keyboard=[["Начало работы"]]

global admin_keyboard
admin_keyboard=[["Заполнить анкету"], ["Распознать человека"], ["Вывести изображение с камеры"], ["Запись видео"], ["Удалить пользователя"]]

global user_keyboard
user_keyboard=[["Заполнить анкету"]]


def stop_video(update, context, e6):
    '''Остановка записи видео'''
    e6.set()
    time.sleep(5)
    e6.clear()

def admin(update, context):
    '''Проверка, к какой группе относится пользователь.'''
    file=open("data/admins.txt", "r")
    info=file.read()
    file.close()
    if info.find(str(update.effective_chat.id))>=0:
        return "a"    
    file=open("data/users.txt", "r")
    info=file.read()
    file.close()
    if info.find(str(update.effective_chat.id))>=0:
        return "p"
    
    return "unknown"

def admin_start(update, context):
    '''Проверка, к какой группе относится пользователь. Если Telegram ID пользователя записан в каком-либо из файлов, пользователю отправляются доступные функции'''
    file=open("data/admins.txt", "r")
    info=file.read()
    file.close()
    if info.find(str(update.effective_chat.id))>=0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Для выполнения какой-либо функции нажмите на соответствующую кнопку", reply_markup=ReplyKeyboardMarkup(admin_keyboard, one_time_keyboard=True))
        return     
    file=open("data/users.txt", "r")
    info=file.read()
    file.close()
    if info.find(str(update.effective_chat.id))>=0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Для заполнения анкеты нажмите на кнопку", reply_markup=ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True))
        return 
    context.bot.send_message(chat_id=update.effective_chat.id, text="Введите пароль")
    return "none"

def none(update, context):
    '''Принимается пароль, если совпадения с паролем администратора или пользователя обнаружено, то ID человека записывается в соответствующий файл'''
    code=update.message.text

    #проверка пароля на администратора
    file=open("data/admin_password.txt", "r")
    info=file.read()
    file.close()
    if code==info:
        file=open("data/admins.txt", "a")
        file.write(str(update.effective_chat.id))
        file.write("\n")
        file.close()      
        context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте, {}! \nПоговори со мной!".format(update.effective_chat.first_name), reply_markup=ReplyKeyboardMarkup(admin_keyboard, one_time_keyboard=True))
        return

    #проверка пароля на обычного пользователя
    file=open("data/user_password.txt", "r")
    info=file.read()
    file.close()
    if info.find(code)>=0:
        file=open("data/users.txt", "a")
        file.write(str(update.effective_chat.id))
        file.write("\n")
        file.close()
        my_keyboard=[["Заполнить анкету"]]
        context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте, {}! \nПоговори со мной!".format(update.effective_chat.first_name), reply_markup=ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True))
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text="Неправильный пароль. Для повторного ввода пароля нажмите кнопку Начало работы", reply_markup=ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True))
    return ConversationHandler.END

def start(update, context, e):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Для начала работы нажмите кнопку Начало работы", reply_markup=ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True))

   
def camera(update, context, e_camera):
    '''Результат функции - изображение, полученное с камеры.'''

    info=admin(update,context)
    if info=="unknown":
        context.bot.send_message(chat_id=update.effective_chat.id, text="У Вас ещё нет прав администратора, для их получения нажмите кнопку Начало работы и введите пароль администратора.", reply_markup=ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True))
    if info=="p":
        context.bot.send_message(chat_id=update.effective_chat.id, text="У Вас нет прав администратора. Вы можете только заполнить анкету", reply_markup=ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True))
    if info=="a":
        e_camera.clear()
        # Включаем первую камеру
        cap = cv2.VideoCapture(0)

        # "Прогреваем" камеру, чтобы снимок не был тёмным
        for i in range(30):
            cap.read()

        # Делаем снимок    
        ret, frame = cap.read()

        # Записываем в файл
        cv2.imwrite('image/cam.png', frame)   

        # Отключаем камеру
        cap.release()
        chat_id = update.effective_chat.id
        context.bot.send_photo(chat_id=chat_id, photo=open("image/cam.png", "rb"))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Функция выполнена.", reply_markup=ReplyKeyboardMarkup(admin_keyboard, one_time_keyboard=True))
        e_camera.set()

def video(update,context):
    info=admin(update,context) #проверка, к какой группе относится пользователь
    if info=="unknown":
        context.bot.send_message(chat_id=update.effective_chat.id, text="У Вас ещё нет прав администратора, для их получения нажмите кнопку Начало работы и введите пароль администратора.", reply_markup=ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True))
    if info=="p":
        context.bot.send_message(chat_id=update.effective_chat.id, text="У Вас нет прав администратора. Вы можете только заполнить анкету", reply_markup=ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True)) 
    
    if info=="a":         
        
        i=0
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
                context.bot.send_message(chat_id=id_chat, text="Для остановки видео нажмите кнопку")
        ids.close()

        while i<60:            
            #e_camera.wait()
            cam = cv2.VideoCapture(0)
            ret, img =cam.read() 
            #if not ret:
            #    e_camera.clear()
            #    e_camera.wait()
            #    cam = cv2.VideoCapture(0)
            #    ret, img =cam.read()

            
            video.write(img) #добавление кадра в видео
            i+=1 #увеличение количества сделанных кадров
            print(i)
                    
        
            #if e6.is_set(): #остановка записи видео
            #   break
        
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