# Expenses management application
This application provides the ability to manage the expenses on the time and cost basis.
Application is built with Python/Django/django-rest-framework/PostgreSQL and React.js on the front-end, packaged with Docker (docker-compose).

## Main features
1. Expenses management. Each expense consists of text, cost, date and time, which you are able to specify, as well add new expenses or create existing ones.
2. Data filtering. Filter expenses based on their data.
3. Role-based permissions system: 
  * Regular user ('user') - only able to work with it's own expenses either by the GUI or API
  * User manager ('user_manager') - only allowed to manage other regular users through corresponding API endpoints
  * Admin ('admin') - full API access.

## Installation
Make sure you have installed Docker.
- ```git clone https://github.com/dmitry-yakutkin/Expenses-App```
- ```cd Expenses-App```
- ```docker-compose up```

Application is now available on port 3000.

## Standard users credentials
Here are some default user's credentials which are present in the system by default in ```login```/```password``` form.
- Regular user: ```user```/```Auph2Aad```
- User manager: ```user_manager```/```yohWoov3```
- Admin: ```admin```/```Yoi9aeMi```