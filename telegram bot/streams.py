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

e_camera=threading.Event()
e6=threading.Event()

def t_stop_video(update, context):
    '''Поток, в котором запускается функция для остановки записи видео.'''
    global e6    
    t6 = threading.Thread(target=stop_video, args=(update, context, e6))
    t6.start()

def t_open_cv(update, context):
    '''Поток, в котором запускается функция "Распознать человека".'''
    global e_camera
    e_camera.set()
    t1 = threading.Thread(target=open_cv, args=(update, context, e_camera))
    t1.start()

def t_start(update, context):
    '''Поток, в котором запускается функция "Начать".'''
    e3=threading.Event()
    t3 = threading.Thread(target=start, args=(update, context, e3))
    t3.start()

def t_camera(update, context):
    '''Поток, в котором запускиется функция "Вывести изображение с камеры".'''
    global e_camera
    t5 = threading.Thread(target=camera, args=(update, context, e_camera))
    t5.start()

def t_get_video_file(update, context):
    '''Поток, в котором запускается функция "Запись видео".'''
    global e6 
    global e_camera
    e_camera.set()
    t6 = threading.Thread(target=get_video_file, args=(update, context, e6, e_camera))
    t6.start()

