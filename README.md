## telegram-bot
Этот Telegram-бот предназначен для распознавания человека по лицу, а также для записи видео, на котором присутствует человек. Пример работы бота можно увидеть здесь: https://yadi.sk/i/UdkvTMX3nEJQoA 
# 1. Создание Telegram-бота.
Для создания бота в Telegram нужно написать боту BotFather, в диалоге с ним сначало нужно отправить команду ``/newbot`` для создания нового бота. Далее нужно ввести название и имя пользователя будущего бота, после чего BotFather отправит ссылку для доступа к боту и его токен.
# 2. Работа с кодом программы.
   Для работы с кодом программы необходимо скачать все прикреплённые файлы в папку проекта. К ним относятся: файлы, содержащие код программы, классификатор лиц, натренированная модель, конфигурационный файл и заранее обученная модель для распознавания образа человека, текстовые файлы: "file_id" (в него записывается номер id последнего зарегистрированного пользователя, сейчас в этом файле записано число 0), "name" (в нём содержаться имена пользователей, сейчас в этом файле первой строчкой записано слово "None", оно соответствует нераспознанному человеку), "info" (в нём должна содержаться информация о возрасте и номерах телефона пользователей, сейчас этот файл пустой), "Администраторы" и "Пользователи" (в них должны находиться Telegram ID администраторов и пользователей, сейчас эти файлы пустые), "пароль админимтратора" и "пароль пользователя" (в этих файлах должны находиться пароли администраторов и пользователей, сейчас эти файлы пустые).
   Первым делом нужно установить все нужные библиотеки.       
	После установки библиотек нужно сделать следующие действия:   
	1. В строке 

	
    $  "updater = Updater(token='Введите Ваш токен API к Telegram')"  
    
   нужно ввести токен, который прислал BotFather.  
    2. В папке проекта нужно создать папку с названием "dataset", она будет служить базой данных изображений лиц пользователя.  
    3. В текстовые "пароль администратора" и "пароль пользователя" нужно вписать соответсвующие пароли.  
    Если Вам будет нужно полностью обновить содержание каких-либо файлов, Вы можете заново скачать эти файлы и создать новый проект.
  # 3. Инструкция по использованию
  Запустить программу на компьютере.  
    Запустите Telegram, нажмите на вкладку вашего бота, нажмите на "/start". После этого Вам отправится первое сообщение от бота и кнопка «Начало работы».  ![Начало работы](https://github.com/k-niiik/telegram-bot/blob/main/PicsArt_01-30-05.59.30.jpg)   При нажатии на эту кнопку  Вам отправится сообщение с запросом пароля, вам нужно ввести пароль админимстратора.  Вам придет сообщение с кнопками доступных функций.  ![Доступные администратору функции](https://github.com/k-niiik/telegram-bot/blob/main/PicsArt_01-30-06.01.28.jpg)  Первым делом вам нужно заполнить анкету, для этого нажмите на кнопку "Заполнить анкету". Введите по порядку Ваше имя, видео с записью Вашего лица (видео должно быть длиною 2-3 секунды, и на нём должно быть хорошо различимо лицо), номер телефона и возраст, в случае, если какие-либо данные введены с ошибкой, у Вас будет возможность ввести их заново. После заполнения анкеты Вам доступен весь функционал бота. ![Начало анкеты](https://github.com/k-niiik/telegram-bot/blob/main/PicsArt_01-30-06.02.25.jpg) ![Проверка анкеты](https://github.com/k-niiik/telegram-bot/blob/main/PicsArt_01-30-06.03.16.jpg) ![Конец анкеты](https://github.com/k-niiik/telegram-bot/blob/main/PicsArt_01-30-06.04.14.jpg)
    
 ---------------
 "Запись видео"
 ---------------  
 
   При нажатии этой кнопки начинается запись видео с камеры тех моментов, когда перед камерой есть человек, и Вам отправится кнопка для её остановки. ![Кнопка для остановки видео](https://github.com/k-niiik/telegram-bot/blob/main/PicsArt_01-30-06.06.09.jpg)  Если человека получится распознать, то будет указано его имя. Если размер видео не будет превышать 100 Мб, то оно будет Вам отправлено.  ![Отправленное видео](https://github.com/k-niiik/telegram-bot/blob/main/PicsArt_01-30-06.07.07.jpg)
   
 ----------------------
 "Распознать человека"
 ----------------------
 
   При нажатии этой кнопки, как только перед камерой появится лицо человека, который есть в базе данных, Вам будет отправлено фото этого человека и его имя.  ![Распознавание человека](https://github.com/k-niiik/telegram-bot/blob/main/PicsArt_01-30-06.08.26.jpg)
   
 ----------------------
 Вывести изображение с камеры"   
 ----------------------
   
   При нажатии этой кнопки Вам будет отправлено фото, сделанное камерой в данный момент.  ![Изображение с камеры](https://github.com/k-niiik/telegram-bot/blob/main/PicsArt_01-30-06.09.16.jpg)
   
----------------------
"Удалить пользователя"
----------------------
     
  При нажатии этой кнопки у Вас будет запрошено имя человека, данные которого надо удалить из базы данных, после чего вся информация о пользователе будет удалена.  ![Удаление пользователя](https://github.com/k-niiik/telegram-bot/blob/main/PicsArt_01-30-06.05.15.jpg)
     
--------------------------------
Функционал обычного пользователя
--------------------------------
     
   Помимо роли администратора, существует роль обычного пользователя, для того, чтобы им стать, на этапе ввода пароля необходимо ввести пароль пользователя. Пользователю позволяется только заполнить анкету.  ![Обычный пользователь](https://github.com/k-niiik/telegram-bot/blob/main/PicsArt_01-30-06.00.26.jpg)  Роль пользователя нужна для того, чтобы человек мог внести свои данные, но не мог удалять чужие данные и не имел доступ к камере.  
     Любой пользователь, не имеющий пароль, не имеет доступа ко всем функциям, пока не введёт пароль.
     
# Рекомендуемые системные требования
- Стибильное подключение к интернету
- Камера с разрешением не менее 480p
- Процессор Intel Pentium Silver N5000 или лучше
- Встроенная графика Intel UHD Graphics 605 или лучше
- Оперативная память минимум 4 Гб
     
#  Источники
[Python-Telegram-Bot](https://github.com/python-telegram-bot/python-telegram-bot).  
[Open CV](https://github.com/opencv/opencv).  
[MobileNetSSD](https://github.com/chuanqi305/MobileNet-SSD).

