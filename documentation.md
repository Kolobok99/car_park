## Содержание:
1. [Титульный лист](#титульный_лист)
2. [Регистрация](#регистрация)
3. [Авторизация](#авторизация_)
4. [Личный кабинет](#личный_кабинет)
6. [Автомобили](#автомобили)
7. [Выбранное авто](#выбранное_авто)
8. [Водители](#водители)
9. [Выбранный водитель](#выбранный_водитель)
10. [Документы](#документы)
11. [Топливные карты](#топливные_карты)
12. [Заявки](#заявки_)
13. [Выбранная заявка](#выбранная_заявка)
14. [История](#история)

12. [Celery](#celery)

13. [Telegram bot](#telegram_bot)

### Титульный лист <a name="титульный_лист"></a>

Идеи и требования к проекту были позаимствованны из портфолио компании [< SMYT >](https://smyt.ru/). С  "ТЗ" проекта можно ознакомиться по [ссылке](https://smyt.ru/projects/sistema-lk-polzovatelej-avtoparka/) или ниже.


**Проект**: Система личных кабинетов администратора автопарка и водителей.

**Описание**:  Наш заказчик – компания, которая предоставляет услуги операционного лизинга автомобилей и услуги управления автопарками своих клиентов. Управление автопарком означает, что наш заказчик берет на себя все заботы по обслуживанию автомобилей своего клиента. Система ведет историю событий, связанных с каждым автомобилем. Клиенты (администраторы автопарка и обычные водители) в своих личных кабинетах по мере необходимоapplications/2сти создают заявки на ремонт и обслуживание своих автомобилей. Наш заказчик принимает заявки в работу и проводит весь необходимый цикл работ по исполнению заявок. Клиенты отслеживают исполнение заявок.

Кроме того, администраторы автопарка на стороне клиента управляют водителями, топливными картами, страховыми полисами, водительскими удостоверениями, медицинскими справками и другими документами.

**Запуск проекта** (деплой проекта был протестирован на Ubuntu 20.04 LTS)
1. Перейти в корень проекта: *cd /car_park/*
2. Собрать докер-образы: *docker-compose -f prod_docker-compose.yml build*
3. Поднять проект *docker-compose -f prod_docker-compose.yml up*


**Задачи**
Личный кабинет администратора автопарка должен выполнять следующие задачи:

-   ведение перечня автомобилей клиента;
-   создание и отслеживание заявок на ремонт автомобилей;
-   автоматическое информирование администратора о неисполненных в срок заявках на ремонт;
-   управление водителями;
-   ведение перечня топливных карт;
-   закрепление автомобилей и топливных карт за водителями;
-   ведение реестров различных документов (страховых полисов, водительских удостоверений, медицинских справок, доверенностей, актов и т. д.);
-   автоматическое информирование администратора об истекающих сроках действия документов;
-   ведение реестра осмотров автомобилей.
- фильтрация основных данных (автомобилей, водителей, документов, заявок, истории)
- ведение истории действий пользователей

Личный кабинет водителя должен выполнять следующие задачи:

-   отображение автомобилей, закрепленных за водителем;
-   создание и отслеживание заявок на ремонт автомобилей;
-   отображение документов (страховых полисов, водительских удостоверений, медицинских справок, доверенностей, актов и т. д.), относящихся к водителю или его автомобилю;
-   автоматическое информирование водителя об истекающих сроках действия документов.

**Технологии:**
- Python
- Django, DRF
- MySQL
- Pytest-Django + Selenium
- HTML, CSS, JS 
- Celery + Redis
- pyTelegramBotAPI
- Docker + docker-compose
- Nginx


### Регистрация <a name="регистрация"></a>


Для того, чтобы начать пользоваться приложением, новому водителю или механику необходимо пройти процесс регистрации.

Для избежания неприятных моментов, связанных с безопасностью, новых администраторов автопарка (далее менеджеров) в системе регистрирует администратор приложения (он же root) в панели django-admin.

**P.S.** Для того, чтобы пройти процесс валидации почты, почта нового пользователя должна быть предварительно добавлена менеджером в таблицу "WhiteEmailList".

Для того, чтобы пройти процесс регистрации, гостю необходимо перейти на стр.
[регистрации](http://car-park.site/registration/)

На этой странице гость видит форму регистрации и кнопку для перехода на стр. "авторизации".
При вводе валидных данных и нажатии кнопки "Отправить",

![Регистрация](https://github.com/Kolobok99/car_park/blob/master/docs_images/image.png)

в таблице MyUser создается запись с новым пользователем и параметром (is_active=False). Гость переадресовывается на стр. 
[активации аккаунта](http://car-park.site/activation/), где ему предлагается ввести код активации, высланный на почту.


![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707175444.png)
<!-- ![[Pasted image 20220707175444.png]] -->


После отправки валидного кода, гость попадает на стр.[авторизации](http://car-park.site/), а его аккаунт становится активным (is_active=True).

**P.S** При отправки невалидных данных, гостю возвращается форма с сообщениями об ошибках.


![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707175954.png)
<!-- ![[Pasted image 20220707175954.png]] -->


### Авторизация <a name="авторизация_"></a>
После прохождения процесса регистрации, водитель (или механик) может авторизироваться в системе, введя корректные данные на стр. [авторизации](http://car-park.site/)

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707180619.png)
<!-- ![[Pasted image 20220707180619.png]] -->
<!-- <br> -->

При вводе невалидных данных, приложение возвращает сообщение об ошибке

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707180907.png)
<!-- ![[Pasted image 20220707180907.png]]. -->
<!-- <br> -->
**P.S.** В независимости от типа невалидных данных (неправильный пароль, неправильная почта, попытка войти в ЛК неактивированного аккаунта), система всегда возвращает одно и тоже сообщение.



### Личный кабинет <a name="личный_кабинет"></a>
После успешной авторизации водитель переадресовывается на стр. [ЛК](http://car-park.site/account/)

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707184920.png)
<!-- ![[Pasted image 20220707184920.png]] -->
<!-- <br> -->

Здесь он может:
- изменять личные данные

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707185435.png)
<!-- ![[Pasted image 20220707185435.png]] -->
<!-- <br> -->

при успешном изменении данных, появляется сообщение:

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707185645.png)
<!-- ![[Pasted image 20220707185645.png]] -->
<!-- <br> -->

P.S. медиа файлы пользователей (аватарки и документы) хранятся в личной папке, которая создается во время регистрации. Название папки совпадает с email'ом. При изменении email'а, название папки также меняется

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707185809.png)
<!-- ![[Pasted image 20220707185809.png]]. -->
<!-- <br> -->

- работать с  закрепленными за ним автомобилями

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707190149.png)
<!-- ![[Pasted image 20220707190149.png]] -->
<!-- <br> -->


При нажатии на *регистрационный номер*, водитель переадресовывается на стр. [выбранного авто](http://car-park.site/cars/F128OS)

- работать с созданными активными заявками

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707190642.png)
<!-- ![[Pasted image 20220707190642.png]] -->
<!-- <br> -->

При нажатии на *название активной заявки*, водитель переадресовывается на стр. [выбранной заявки](http://car-park.site/applications/1)

- изменять баланс закрепленной за ним топливной карты

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707190910.png)
<!-- ![[Pasted image 20220707190910.png]]. -->
<!-- <br> -->

При успешном изменении баланса 
*(баланс должен быть >= 0 и <= лимиту)*
Появляется сообщение:

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707191030.png)
<!-- ![[Pasted image 20220707191030.png]] -->
<!-- <br> -->

- добавлять и удалять персональные документы:
При нажатии на кнопку "добавить" (документ), появляется форма:


<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220803130621.png)
<!-- ![[Pasted image 20220803130621.png]]. -->
При отправки валидных данных (здесь невалидным может быть только *дата окончания*, она должна быть больше *даты выдачи*), появляется сообщение:
<!-- <br> -->

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707191336.png)
<!-- ![[Pasted image 20220707191336.png]] -->
и новая запись в таблице.
<!-- <br> -->

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707191407.png)
<!-- ![[Pasted image 20220707191407.png]] -->
При вводе невалидной даты, форма возвращается с сообщением об ошибке:
<!-- <br> -->

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707191904.png)
<!-- ![[Pasted image 20220707191904.png]] -->
<!-- <br> -->

При нажатии на кнопку "удалить" (определенный документ), появляется окно подтверждения:

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707191600.png)
<!-- ![[Pasted image 20220707191600.png]] -->
<!-- <br> -->

При нажатии кнопки "да" (удалить!), появляется сообщение:

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707191627.png)
<!-- ![[Pasted image 20220707191627.png]] -->
<!-- <br> -->

и запись с ранее созданным документом пропадает:

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707191740.png)
<!-- ![[Pasted image 20220707191740.png]] -->
<!-- <br> -->

**Также** стоит отметить, что водитель, хоть и видит меню сайта,

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707192013.png)
<!-- ![[Pasted image 20220707192013.png]] -->
<!-- <br> -->

но при попытке перехода на любую из страниц, он получает сообщение:

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707192049.png)
<!-- ![[Pasted image 20220707192049.png]] -->
<!-- <br> -->

**Также**, при попытке попасть на стр. чужой машины или заявки:

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220707192049.png)
<!-- ![[Pasted image 20220707192049.png]] -->
<!-- <br> -->

### Автомобили <a name="автомобили"></a>
Перейдя на стр. [автомобили](http://car-park.site/cars/), менеджер:

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220729172557.png)
<!-- ![[Pasted image 20220729172557.png]] -->
<!-- <br> -->

- видит общее кол-во (или кол-во отфильтрованных) авто;

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708140121.png)
<!-- ![[Pasted image 20220708140121.png]] -->
<!-- <br> -->

- может добавить новое авто. При нажатии на кнопку "добавить авто", открывается форма;

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708140243.png)
<!-- ![[Pasted image 20220708140243.png]] -->
<!-- <br> -->

При введении корректных данных и нажатии кнопки "отправить", новое авто появляется в таблице.
При введении некорректных данных, форма возвращается с сообщениями об ошибках.

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708140450.png)
<!-- ![[Pasted image 20220708140450.png]] -->
<!-- <br> -->

- фильтровать автомобили по их параметрам;

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708140539.png)
<!-- ![[Pasted image 20220708140539.png]] -->
<!-- <br> -->

- удалять и изымать выбранные автомобили.

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708141109.png)
<!-- ![[Pasted image 20220708141109.png]] -->
<!-- <br> -->



### Выбранное авто <a name="выбранное_авто"></a>
После нажатия на регистрационный номер выбранного авто, владелец авто или менеджер попадает на соответствующую стр. [страницу ](http://car-park.site/cars/F128OS)

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708130148.png)
<!-- ![[Pasted image 20220708130148.png]] -->
<!-- <br> -->

P.S. в отличии от водителя, менеджер имеет возможность менять информацию об авто

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708130350.png)
<!-- ![[Pasted image 20220708130350.png]] -->
<!-- <br> -->

Здесь владелец авто и менеджер могут:
- Просматривать ранее созданные заявки и переходить на [стр. заявки](http://car-park.site/applications/1) путем нажатия по ее ID.
- Добавлять  новые заявки. При нажатии на кнопку добавить (заявку), открывается форма добавления заявки.

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708132416.png)
<!-- ![[Pasted image 20220708132416.png]] -->
<!-- <br> -->

Форма менеджера отличается наличием поля выбора механика.

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220729172325.png)
<!-- ![[Pasted image 20220729172325.png]] -->
<!-- <br> -->

После нажатия кнопки отправить, новая заявка появляется в таблице.
- таблица Документы, идентична таблице Документы на стр. ЛК.

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708132607.png)
<!-- ![[Pasted image 20220708132607.png]] -->
<!-- <br> -->

### Водители <a name="водители"></a>
Стр. [водители](http://car-park.site/drivers/) аналогична стр. Автомобили, за исключением возможности добавления новых водителей.

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708140801.png)
<!-- ![[Pasted image 20220708140801.png]] -->
<!-- <br> -->

### Выбранный водитель <a name="выбранный_водитель"></a>
Стр. [Выбранного водителя](http://car-park.site/drivers/4) отображает всю информацию о нем и связанных с ним записях.

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708143423.png)
<!-- ![[Pasted image 20220708143423.png]] -->
<!-- <br> -->

Также на этой стр. имеется возможность присвоить водителю одну из свободных топливных карт.

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708143459.png)
<!-- ![[Pasted image 20220708143459.png]] -->
<!-- <br> -->


### Документы <a name="документы"></a>
Стр. [документы](http://car-park.site/documents/) отличается от стр. Водители одновременной работой c двумя таблицами: "документы авто" и "документы водителей".

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708141014.png)
<!-- ![[Pasted image 20220708141014.png]] -->
<!-- <br> -->

### Топливные карты <a name="топливные_карты"></a>
стр. [топливные карты](http://car-park.site/cards/) идентична стр. Автомобили.

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708141158.png)
<!-- ![[Pasted image 20220708141158.png]] -->
<!-- <br> -->

### Заявки <a name="заявки_"></a>
стр. [заявки](http://car-park.site/applications) идентична стр. Водители.

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708141237.png)
<!-- ![[Pasted image 20220708141237.png]] -->
<!-- <br> -->

### Выбранная заявка <a name="выбранная_заявка"></a>
После создания заявки (водителем), ей присваивается первичный статус: "Ожидает рассмотрения". 

Перейдя на [стр. заявки](http://car-park.site/applications/1/), **владелец** заявки, может:

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708133714.png)
<!-- ![[Pasted image 20220708133714.png]] -->
<!-- <br> -->

- ознакомиться со всей информацией;
- изменить заявку, нажав на кнопку "Изменить заявку". Появится форма, аналогичная форме на стр. выбранное авто;

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220729172455.png)
<!-- ![[Pasted image 20220729172455.png]] -->
<!-- <br> -->

- удалить заявку. При нажатии на кнопку "Удалить заявку", появится форма подтверждения.

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708133756.png)
<!-- ![[Pasted image 20220708133756.png]] -->
<!-- <br> -->

**Менеджер** при переходе на чужую заявку, может:

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708133845.png)
<!-- ![[Pasted image 20220708133845.png]] -->
<!-- <br> -->

- Одобрить заявку, нажав на кнопку "Подтвердить". После отправки формы, заявке присвоится статус "Ожидает  рассмотрения механика";

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708134114.png)
<!-- ![[Pasted image 20220708134114.png]] -->
<!-- <br> -->
- Отклонить заявку, нажав на кнопку "Вернуть на доработку". После подтверждения, заявке присвоится статус "Отклонена".

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708134223.png)
<!-- ![[Pasted image 20220708134223.png]] -->
<!-- <br> -->

### История <a name="история"></a>
стр. [история](http://car-park.site/history/) отображает всю историю действий пользователей. Также есть возможность фильтровать историю по времени, типу и статусу.

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708141456.png)
<!-- ![[Pasted image 20220708141456.png]] -->
<!-- <br> -->




### Celery <a name="celery"></a>
Для обработки фоновых и переодических задач была использована программа celery и redis в качестве брокера задач.  
Реализованные задачи:

фоновые задачи:

-   отправка кода активации аккаунта на email user'а.

переодические задачи:

-   создание заявки на плановый осмотр авто;
-   создание уведомления об истекающем сроке действия документов;
-   удаление "пустых" топливных карт;
-   создание уведомлений о том, что заканчиваются топливные карты;
-   создание уведомлений о просроченных заявках.

### TelegramBot <a name="telegram_bot"></a>
Телеграмм бот разработан в качестве дополнения к веб-приложению "CarPark".
Основной функционал:
- Отправка уведомлений пользователям;
- Обработка заявок (механиками).

#### Авторизация
При первом запуске телеграмм бота (вводе команды /start), он просит доступ к номеру телефону. Номер телефона должен совпадать с номером, указанным во время регистрации.

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708155138.png)
<!-- ![[Pasted image 20220708155138.png]] -->
<!-- <br> -->

После отправки номера и его успешной валидации, пользователь получает доступ к главному меню.

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708155522.png)
<!-- ![[Pasted image 20220708155522.png]] -->
<!-- <br> -->

#### Уведомления
После нажатия кнопки "уведомления", пользователь из основного меню попадает в меню активные уведомления.

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708164124.png)
<!-- ![[Pasted image 20220708164124.png]] -->
<!-- <br> -->

Используя "<<" и "">>" можно перемещаться между уведомлениями

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708164226.png)
<!-- ![[Pasted image 20220708164226.png]]. -->
<!-- <br> -->
Кнопка "подтвердить" делает уведомление просмотренным.

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708164339.png)
<!-- ![[Pasted image 20220708164339.png]] -->
<!-- <br> -->

#### Заявки
После нажатия кнопки "Заявки", пользователь из основного меню попадает в меню заявки.

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708174231.png)
<!-- ![[Pasted image 20220708174231.png]] -->
<!-- <br> -->

Нажатие кнопки "Новые заявки" генерирует первую заявку, рассмотренную менеджером. Нажатие кнопки "Приступить к ремонту", изменяет статус заявки на "Ремонтируется" и удаляет ее из списка новых заявок!

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708174731.png)
<!-- ![[Pasted image 20220708174731.png]] -->
<!-- <br> -->

Нажатие кнопки "Приступить к ремонту", изменяет статус заявки на "Ремонтируется" и удаляет ее из списка новых заявок!

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708174746.png)
<!-- ![[Pasted image 20220708174746.png]] -->
<!-- <br> -->

После завершение ремотных работ, механик должен перейти в меню "Активные заявки" и нажать кнопку "Выполнить заявку".

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708175015.png)
<!-- ![[Pasted image 20220708175015.png]] -->
<!-- <br> -->

Если кнопка выполнения заявки была нажата по ошибке, есть возможность вернуть заявке статус *ремонтируется*, перейдя в раздел меню "Выполненные заявки" и нажав кнопку "Доработать заявку".

<!-- <br> -->
![](https://github.com/Kolobok99/car_park/blob/master/docs_images/Pasted%20image%2020220708175209.png)
<!-- ![[Pasted image 20220708175209.png]] -->
<!-- <br> -->
