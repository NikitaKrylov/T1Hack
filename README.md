<br />
<div align="center">
    <img src="static/sprint-pulse-logo.svg" alt="Logo" width="300" height="80">

  <h3 align="center">MISIS 52</h3>
  <p align="center">
    <a href="https://disk.yandex.ru/i/t0TaaEokOw07Iw"><strong>Презентация »</strong></a>
    <br />
    <a href="https://open-your-smolensk.ru/"><strong>Попробовать »</strong></a>
    <br />
    </p>
</div>

# Цель проекта 
Создание платформы и/или онлайн-инструмента, которая будет служить центром для продвижения цифрового искусства и креативной экономики в Смоленске.

# О Проекте
Айвазовский — это платформа для цифрового искусства в Смоленске, объединяющая творчество и бизнес, с уникальными NFC-метками для оживления городских пространств.

## Требования 

Для локальной установки и использования сервиса вам потребуется docker compose и установленный git.

## Установка 
Скачайте и перейдите в директорию проекта.
```zsh
git clone https://github.com/NikitaKrylov/T1Hack.git # клонирование репозитория
cd T1Hack # переход в рабочую директорию
```

Далее нужно создать и настроить *.env файлы. Требуется создать и заполнить следующие файлы:
- .env
- db.env
- backend.env
- redis.env

> В файле backend.env поле MODE может принимать значения PROD или DEV. Для локального запуска нужно выставить DEV

Примерами заполненных файлов являются файлы *.env.example. Они так же лежат в директориях, которых должны находиться целевые файлы.

После чего нужно запустить проект.
```zsh
docker copmose up --build -d # создание и запуск контейнеров
docker exec -it backend alembic upgrade head # применение миграций базы данных 
```



