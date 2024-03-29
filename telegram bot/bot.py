# Настройки
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
from streams import *
import concurrent.futures
from datetime import datetime, date, time







updater = Updater(token='Введите Ваш токен API') # Токен API к Telegram
dispatcher = updater.dispatcher

#уведомление администраторов о запуске программы
ids=open("data/admins.txt", "r")
for num, line in enumerate(ids, 0):
    print (line)
    if len(line)>1:
        id_chat=line
        updater.bot.send_message(chat_id=id_chat, text="Программа запущена. Можете воспользоваться доступными функциями.", reply_markup=ReplyKeyboardMarkup(admin_keyboard, one_time_keyboard=True))   
ids.close()
print ("Программа запущена")

    


# Обработка команд
def main():
    
    start_handler = CommandHandler('start', t_start)
    dispatcher.add_handler(MessageHandler(Filters.regex("Запись видео"), t_get_video_file))
    dispatcher.add_handler(MessageHandler(Filters.regex("Начать"), t_start))
    dispatcher.add_handler(MessageHandler(Filters.regex("Вывести изображение с камеры"), t_camera))
    dispatcher.add_handler(MessageHandler(Filters.regex("Оcтановить запись видео"), t_stop_video))    
    dispatcher.add_handler(MessageHandler(Filters.regex("Распознать человека"), t_open_cv))
    dispatcher.add_handler(MessageHandler(Filters.regex("Непрерывная запись видео"), video))

    #диалоги
    dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex("Заполнить анкету"), anketa_start)], states={
       "get_name": [MessageHandler(Filters.text, get_name)],
       "get_video": [MessageHandler(Filters.video, get_video)],
       "number": [MessageHandler(Filters.text, number)],
       "age": [MessageHandler(Filters.text, age)],
       "get_choice" : [MessageHandler(Filters.text, get_choice)],
       "anketa_start" : [MessageHandler(Filters.text, anketa_start)],
              },
       fallbacks=[]
       )
)

    dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex("Удалить пользователя"), delete_person)], states={
        "person_name": [MessageHandler(Filters.text, person_name)],
         },
       fallbacks=[]
       )
)

    dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex("Начало работы"), admin_start)], states={
        "none": [MessageHandler(Filters.text, none)]      
         },
       fallbacks=[]
       )
)
    
    dispatcher.add_handler(start_handler)
   
    # Начинаем поиск обновлений
    updater.start_polling(clean=True)
    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()

    
    
    



if __name__=="__main__":
    main()
   