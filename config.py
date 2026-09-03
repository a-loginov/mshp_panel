# Главный способ для запуска в дериктории должен быть .env #

import os
from dotenv import load_dotenv


load_dotenv()


# Секретный ключ Flask #
SECRET_KEY=os.environ["SECRET_KEY"]