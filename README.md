## Задача
Необходимо разработать сервис управления рассылками API администрирования и получения статистики.

## Описание

* Необходимо реализовать методы создания новой рассылки, просмотра созданных и получения статистики по выполненным рассылкам.
* Реализовать сам сервис отправки уведомлений на внешнее API.
* Опционально вы можете выбрать любое количество дополнительных пунктов описанных после основного.
Для успешного принятия задания как выполненного достаточно корректной и рабочей реализации требований по основной части, но дополнительные пункты помогут вам продемонстрировать ваши навыки в смежных технологиях.

***

### Запуск.

* python3 -m venv venv              создаем виртуальное окружение.
* 
* source venv/bin/activate          активация виртуального окружения.
* 
* pip install -r requirements.txt   устанавливаем зависимости.
* 
* В PostgreSQL создаем бд с названием postgres (имеется по дефолту). DNS для подключения postgresql://127.0.0.1:5432/postgres
* 
* Выполняем запрос из фаила db.sql в PostgreSQL (создаем таблицы и тестовые данные).
*
* uvicorn main:app                  зарускаем сервер.

### Маршруты.

* http://127.0.0.1:8000/docs            Описание всех маршрутов, там же можно и по тестить.
* 
* http://127.0.0.1:8000/client/add      Добавление нового клиента. При успешном добавлении возвращает статус 201 и тело {"status": "ok"}
*
* http://127.0.0.1:8000/client/update/{id_client}  Редактирование имеющегося клиента. При успехе возвращает статус 200 и тело измененого клиета.
При неизвестном клиенте возвращает статус 40 тело {"detail": "Client not found"}






