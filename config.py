# Главный способ для запуска в дериктории должен быть .env #

import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла.
# Это позволяет запускать приложение локально без Docker,
# прочитав конфигурацию из файла .env.
load_dotenv()


# IOT-Ключ для устройств #
IOT_KEY=os.environ["IOT_KEY"]


# Секретный ключ Flask #
SECRET_KEY=os.environ["SECRET_KEY"]

# База данных (PostgreSQL) #
DATABASE_URL=os.environ["DATABASE_URL"]

# Пароль администратора #
ADMIN_PASSWORD=os.environ["ADMIN_PASSWORD"]