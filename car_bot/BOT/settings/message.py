# импортируем настройки для отражения эмоджи
from .config import VERSION, AUTHOR


notifications = """
УВЕДОМЛЕНИЕ № {}
дата: {}
сообщение: {}
"""

settings = """
<i>Общая информация:</i>
Данный чат бот разработан 
как дополнение к программе CarPark

<i>Функционал:</i>

- Получение уведомлений
- Получение заявок на ремонт (МЕХАНИКИ)
 
-<b>версия программы: - </b><i>({})</i>
-<b>разработчик: - </b><i>({})</i>


""".format(
    VERSION,
    AUTHOR,
)

applications = """
ЗАЯВКА НОМЕР:           {}
МАШИНА                  {}
ТИП:                    {}
ОПИСАНИЕ:               {}
КОММЕНТАРИЙ МЕНЕДЖЕРА:  {}
ВЫПОЛНИТЬ ДО:           {}
"""

# словарь ответов пользователю
MESSAGES = {
    'notifications': notifications,
    'applications': applications
}
