# HR

Przykładowy projekt w Django.
Prosty system będący uzupełnieniem głównego systemu ERP biura rachunkowego.
Działający w oparciu o bazę danych MS SQL.
Umożliwia pogląd danych kadrowych w trybie tylko do odczytu dla Klientów biura.
Oraz zapewnia dodatkowe możliwości generowania dokumentów i imporów danych dla Pracowników biura.


# Uruchomienie projektu

1) Zainstalowanie wszystkich pakietów z requirements.txt
2) Skonfigurowanie połączenia bazy danych MS SQL:
```python
DATABASES = {
    'default': {

        "ENGINE": "mssql",
        "NAME": "db_name",
        "USER": "user_name",
        "PASSWORD": database_password,
        "HOST": "localhost",
        "PORT": "1433",
        "OPTIONS": {"driver": "ODBC Driver 17 for SQL Server",
                    },
    }
}

```

3) Dodanie pliku .env i podanie hasła do bazy danych

    ```dotenv
    DATABASE_PASSWORD = <password>
    ```
4) Uruchomienie migracji poleceniem migrate
5) Uruchomienie aplikacji
7) Przykładowy plik do testów importu employee/import_test.csv
