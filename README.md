# SCD - Tema 2 - Microservicii & Docker

## Descriere

Am folosit FastAPI cu MongoDB pentru a crea un REST API care sa ofere functionalitatile CRUD pentru entitățile Country, City și Temperature. 
Această aplicație este containerizată folosind Docker și este orchestrată folosind Docker Compose.
De asemenea avem și un utiliar de gestiune a bazei de date MongoDB - Mongo Express.

### REST API

- **Country**
  - **POST** /api/countries - Adaugă o țară
  - **GET** /api/countries - Returnează toate țările
  - **PUT** /api/countries/{country_id} - Actualizează țara cu id-ul specificat
  - **DELETE** /api/countries/{country_id} - Șterge țara cu id-ul specificat
  
- **City**
  - **POST** /api/cities - Adaugă un oraș
  - **GET** /api/cities - Returnează toate orașele
  - **GET** /api/cities/country/{country_id} - Returnează toate orașele din țara cu id-ul specificat
  - **PUT** /api/cities/{city_id} - Actualizează orașul cu id-ul specificat
  - **DELETE** /api/cities/{city_id} - Șterge orașul cu id-ul specificat

- **Temperature**
  - **POST** /api/temperatures - Adaugă o temperatură
  - **GET** /api/temperatures?lat=Double&lon=Double&from=Date&until=Date - Returnează toate temperaturile pentru coordonatele specificate sau pentru un interval de timp
  - **GET** /api/temperatures/cities/:id_oras?from=Date&until=Date - Returnează toate temperaturile pentru orașul cu id-ul specificat sau pentru un interval de timp
  - **GET** /api/temperatures/countries/:id_tara?from=Date&until=Date - Returnează toate temperaturile pentru orașul cu id-ul specificat sau pentru un interval de timp
  - **PUT** /temperatures/{temperature_id} - Actualizează temperatura cu id-ul specificat
  - **DELETE** /temperatures/{temperature_id} - Șterge temperatura cu id-ul specificat

### Docker

- **MongoDB** - Baza de date
- **Mongo Express** - Interfață web pentru gestionarea bazei de date
- **FastAPI** - REST API

## Rulare

Adăugați în fișierul `.env` variabilele de mediu pentru a configura aplicația.
Un exemplu de fișier `.env` ar fi:

```
APP_PORT=5000

MONGO_PORT=27017

MONGO_EXPRESS_PORT=8081
ME_CONFIG_MONGODB_SERVER=mongo
ME_CONFIG_MONGODB_PORT=${MONGO_PORT}
ME_CONFIG_MONGODB_ENABLE_ADMIN=true
ME_CONFIG_BASICAUTH_USERNAME=admin
ME_CONFIG_BASICAUTH_PASSWORD=strongpassword
```

Rulează aplicația folosind Docker Compose în directorul proiectului:

```
docker compose up
```