# Public-Catering-Check
Программа для учета проверок крупной сети столовых и получения обобщённых сведений о результатах проверок.

## Установка
1) `git clone https://github.com/Votchitsev/RusPir-PublicCateringCheck.git`
2) `cd RusPir-PuplicCateringCheck`
3) `python3 -m venv venv`
4) `source venv/bin/activate`
5) `pip install -r requirements.txt`
6) в директории `check_list` создаём файл `secret_key.txt` и в первой строчке записываем секретный ключ (любой).
7) запускаем проект: `python3 manage.py runserver <порт>`