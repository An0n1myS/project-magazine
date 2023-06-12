Цей репозиторій містить код для проекту "Magazine" - веб-додатку для онлайн-журналу. Проект розроблений командою An0n1myS.

Опис проекту
"Magazine" - це веб-додаток, який дозволяє користувачам створювати, редагувати і публікувати статті в онлайн-журналі. Користувачі можуть створювати облікові записи, входити до системи і взаємодіяти з іншими користувачами, коментувати статті та виставляти оцінки.

Основні можливості
Реєстрація та аутентифікація користувачів
Створення, редагування та видалення статей
Пошук статей за ключовими словами або категоріями
Коментування статей
Виставлення оцінок статтям
Можливість підписуватися на авторів статей та отримувати сповіщення про нові публікації
Технології
Проект "Magazine" реалізований з використанням наступних технологій:

Python: мова програмування для реалізації серверної логіки
Django: веб-фреймворк для розробки веб-додатків
HTML/CSS: для розмітки та стилізації веб-сторінок
JavaScript: для інтерактивності та взаємодії з користувачем
SQLite: база даних для збереження інформації про користувачів, статті, коментарі та оцінки
Установка
Склонуйте репозиторій:
bash
Copy code
git clone https://github.com/An0n1myS/project-magazine.git
Перейдіть до директорії проекту:
bash
Copy code
cd project-magazine
Створіть та активуйте віртуальне середовище:
bash
Copy code
python -m venv venv
source venv/bin/activate
Встановіть необхідні залежності:
bash
Copy code
pip install -r requirements.txt
Застосуйте міграції для створення бази даних:
bash
Copy code
python manage.py migrate
Запустіть сервер розробки:
bash
Copy code
python manage.py runserver
