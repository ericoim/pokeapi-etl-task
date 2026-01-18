# Pokémon Scouting Data Application

A Flask-based application that retrieves, processes, and stores Pokémon data using the PokeAPI.

## Project Structure

The project follows a Clean Architecture approach with a **Repository-Service-Controller** pattern:

```
pokemon_app/
├── __init__.py             # Application factory
├── api/                    # Presentation Layer
│   ├── __init__.py         # API blueprint
│   └── controller.py       # Request handling and HTTP responses
├── model/                  # Domain Layer
│   └── pokemon.py          # Database entity definitions
├── repository/             # Data Access Layer
│   └── pokemon_repo.py     # Database abstractions
├── service/                # Business Logic Layer
│   ├── pokemon_svc.py      # Core business logic (typo fixing, idempotency)
│   └── pokeapi.py          # External API adapter
├── logger/                 # Observability
│   └── logger.py           # Centralized logging configuration
└── config.py               # Application settings
```

## Setup Instructions

1. Creating virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

2. Installing dependencies:
```bash
pip install -r requirements.txt
```

3. Running the application:
```bash
python run.py
```
*Note: On the first run, the application will automatically perform a batch sync of the default Pokémon list.*

## API Endpoints

### List all Pokémon
```bash
curl http://localhost:5000/api/v1/pokemon
```

### Refresh Pokémon data
Triggers a manual sync of the configured Pokémon list.
```bash
curl -X POST http://localhost:5000/api/v1/refresh
```

### Get a specific Pokémon
```bash
curl http://localhost:5000/api/v1/pokemon/pikachu
```

### Add a new Pokémon
Fetches data from PokeAPI and stores it locally.
```bash
curl -X POST http://localhost:5000/api/v1/pokemon/pikachu
```

### Update a specific Pokémon Data
Refreshes the local data from PokeAPI.
```bash
curl -X PUT / PATCH http://localhost:5000/api/v1/pokemon/pikachu
```

### Remove a specific Pokémon
```bash
curl -X DELETE http://localhost:5000/api/v1/pokemon/pikachu
```

## Default Configuration

As per request, this application is configured to fetch data for the following Pokémon - stored in `config.py`:
- Pikachu
- Dhelmise
- Charizard
- Parasect
- Aerodactyl
- Kingler

## Database

This application uses **SQLite** with **SQLAlchemy ORM**, as per recommendation / request.
The DB `pokemon.db` is automatically created when you first run it.

## Architecture & Development

This project emphasizes *Separation of Concerns* in its design:
- **Controller** `(api/controller.py)` - Handles HTTP requests and responses. Contains no business logic by design.
- **Service** `(service/pokemon_svc.py)` - The brain of the application. Handles data normalization (fixing typos), idempotency checks, and orchestration.
- **Repository** `(repository/pokemon_repo.py)` - Abstracts the database layer. The Service layer does not know it is speaking to SQL.
- **Adapter** `(service/pokeapi.py)` - A dedicated client for external API communication, handling timeouts and error logging.

This structure allows for a lower level of coupling, making it possible for any hypothetical future changes to involve less impact in surrounding components - i.e.: a change in DB driver will be contained in the Repository layer, while maintaining code in the Service Layer untouched.