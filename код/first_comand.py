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
    '''Проверка, к какой группе относится пользователь'''
    file=open("Администраторы.txt", "r")
    info=file.read()
    file.close()
    if info.find(str(update.effective_chat.id))>=0:
        return "a"    
    file=open("Пользователи.txt", "r")
    info=file.read()
    file.close()
    if info.find(str(update.effective_chat.id))>=0:
        return "p"
    
    return "unknown"
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Введите пароль")
    return "none"
def none(update, context):
    '''Принимается пароль, если совпадения с паролем администратора или пользователя обнаружено, то ID человека записывается в соответствующий файл'''
    code=update.message.text

    #проверка пароля на администратора
    file=open("пароль администратора.txt", "r")
    info=file.read()
    file.close()
    if code==info:
        file=open("Администраторы.txt", "a")
        file.write(str(update.effective_chat.id))
        file.write("\n")
        file.close()      
        context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте, {}! \nПоговори со мной!".format(update.effective_chat.first_name), reply_markup=ReplyKeyboardMarkup(admin_keyboard, one_time_keyboard=True))
        return

    #проверка пароля на обычного пользователя
    file=open("пароль пользователя.txt", "r")
    info=file.read()
    file.close()
    if info.find(code)>=0:
        file=open("Пользователи.txt", "a")
        file.write(str(update.effective_chat.id))
        file.write("\n")
        file.close()
        my_keyboard=[["Заполнить анкету"]]
        context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте, {}! \nПоговори со мной!".format(update.effective_chat.first_name), reply_markup=ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True))
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text="Неправильный пароль")

def start(update, context, e):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Для начала работы нажмите кнопку Начало работы", reply_markup=ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True))

   
def camera(update, context, e_camera):
    '''Результат функции - изображение, полученное с камеры.'''

    info=admin(update,context)
    if info=="unknown":
        context.bot.send_message(chat_id=update.effective_chat.id, text="У Вас ещё нет прав администратора, для их получения нажмите кнопку Начало работы и введите пароль администратора.", reply_markup=ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True))
    if info=="p":
        context.bot.send_message(chat_id=update.effective_chat.id, text="У Вас нет прав администратора.")
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
        cv2.imwrite('cam.png', frame)   

        # Отключаем камеру
        cap.release()
        chat_id = update.effective_chat.id
        context.bot.send_photo(chat_id=chat_id, photo=open("cam.png", "rb"))
        e_camera.set()

