# Lancer Reserves API

A REST and GraphQL API for managing Lancer TTRPG reserves, built with FastAPI, SQLAlchemy, and Strawberry GraphQL.

## Features

- ✅ RESTful API with full CRUD operations
- ✅ GraphQL API with queries and mutations
- ✅ Automatic Swagger/OpenAPI documentation
- ✅ SQLite database with automatic seeding from `reserves.json`
- ✅ Support for all four reserve types: Bonus, Resource, Mech, and Tactical
- ✅ Flexible data model supporting bonuses, deployables, actions, and synergies

## Reserve Types

### Bonus
Reserves that grant character advancement points:
- Skill Point
- Mech Skill Point
- Talent Point
- License Point
- Extra CORE Bonus

### Resource
Mission resources and advantages:
- Access
- Backing
- Supplies
- Disguise
- Diversion
- Blackmail
- Reputation
- Safe Harbor
- Tracking
- Knowledge

### Mech
Mech-specific enhancements:
- Ammo
- Rented gear
- Extra repairs
- CORE battery
- Deployable Shield
- Redundant repair
- Systems reinforcement
- Smart ammo
- Boosted servos
- Jump jets

### Tactical
Mission-level tactical advantages:
- Scouting
- Vehicle
- Reinforcements
- Environmental shielding
- Accuracy
- Bombardment
- Extended Harness
- Ambush
- Orbital Drop
- NHP Assistant

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd lancer_reserves
```

2. **Install uv (if not already installed)**
```bash
# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **Create virtual environment and install dependencies**
```bash
uv sync
```

4. **Run the application**
```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **GraphQL Playground**: http://localhost:8000/graphql

## REST API Endpoints

### Base URL: `/api/v1/reserves`

#### Create a Reserve
```http
POST /api/v1/reserves
Content-Type: application/json

{
  "id": "reserve_custom",
  "name": "Custom Reserve",
  "type": "Tactical",
  "label": "Resource",
  "description": "A custom reserve for testing"
}
```

#### List All Reserves
```http
GET /api/v1/reserves?type=Mech&skip=0&limit=100
```

Query parameters:
- `type`: Filter by reserve type (Bonus, Resource, Mech, Tactical)
- `label`: Filter by label (case-insensitive search)
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 100, max: 1000)

#### Get Reserve by ID
```http
GET /api/v1/reserves/{reserve_id}
```

#### Get Reserves by Type
```http
GET /api/v1/reserves/type/Tactical
```

#### Get Random Reserves
```http
GET /api/v1/reserves/random?count=3&type=Mech
```

Query parameters:
- `count`: Number of random reserves to return (default: 1, max: 50)
- `type`: Optional filter by reserve type before random selection

#### Update a Reserve
```http
PUT /api/v1/reserves/{reserve_id}
Content-Type: application/json

{
  "name": "Updated Name",
  "description": "Updated description"
}
```

#### Delete a Reserve
```http
DELETE /api/v1/reserves/{reserve_id}
```

#### Bulk Import Reserves
```http
POST /api/v1/reserves/import
Content-Type: application/json

[
  {
    "id": "reserve_test1",
    "name": "Test Reserve 1",
    "type": "Bonus",
    "label": "Bonus",
    "description": "Test description"
  }
]
```

## GraphQL API

### Endpoint: `/graphql`

#### Example Queries

**Get all reserves:**
```graphql
query {
  reserves {
    id
    name
    type
    label
    description
    createdAt
    updatedAt
  }
}
```

**Get reserves by type:**
```graphql
query {
  reserves(type: MECH) {
    id
    name
    label
    bonuses {
      id
      val
    }
  }
}
```

**Get specific reserve:**
```graphql
query {
  reserve(id: "reserve_skill") {
    id
    name
    type
    label
    description
    bonuses {
      id
      val
    }
  }
}
```

**Search by label:**
```graphql
query {
  reservesByLabel(label: "Resource") {
    id
    name
    label
  }
}
```

**Get random reserves:**
```graphql
query {
  randomReserves(count: 3, type: MECH) {
    id
    name
    type
    label
    description
  }
}
```

#### Example Mutations

**Create a reserve:**
```graphql
mutation {
  createReserve(input: {
    id: "reserve_custom"
    name: "Custom Reserve"
    type: TACTICAL
    label: "Resource"
    description: "A custom tactical reserve"
  }) {
    id
    name
    type
    createdAt
  }
}
```

**Update a reserve:**
```graphql
mutation {
  updateReserve(
    id: "reserve_custom"
    input: {
      name: "Updated Custom Reserve"
      description: "Updated description"
    }
  ) {
    id
    name
    description
    updatedAt
  }
}
```

**Delete a reserve:**
```graphql
mutation {
  deleteReserve(id: "reserve_custom")
}
```

**Bulk import:**
```graphql
mutation {
  importReserves(reserves: [
    {
      id: "reserve_test1"
      name: "Test Reserve"
      type: BONUS
      label: "Bonus"
      description: "Test description"
    }
  ]) {
    id
    name
  }
}
```

## Data Model

### Reserve
All reserves contain:
- `id` (string): Unique identifier
- `name` (string): Display name
- `type` (enum): Bonus, Resource, Mech, or Tactical
- `label` (string): Category label
- `description` (string): HTML-compatible description
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

### Optional Fields
- `bonuses`: Array of `{id: string, val: int}`
- `deployables`: Array of deployable definitions
- `actions`: Array of activatable actions with range/damage
- `synergies`: Array of synergy effects

## Database

The application uses SQLite with automatic initialization. On first run, it will:

1. Create the `lancer_reserves.db` database file
2. Create all necessary tables
3. Import data from `reserves.json` if present

The database file is created in the project root directory.

## Development

### Project Structure
```
lancer_reserves/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models/
│   │   └── reserves.py      # SQLAlchemy models
│   ├── schemas/
│   │   └── reserves.py      # Pydantic schemas
│   ├── api/
│   │   └── v1/
│   │       └── reserves.py  # REST endpoints
│   └── graphql/
│       ├── schema.py        # GraphQL types
│       ├── queries.py       # GraphQL queries
│       └── mutations.py     # GraphQL mutations
├── reserves.json            # Source data
├── pyproject.toml           # Project configuration and dependencies
├── uv.lock                  # Dependency lock file
└── README.md
```

### Running Tests

```bash
# Install test dependencies and run tests
uv sync --dev
uv run pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Data structure based on [massif-press/lancer-data](https://github.com/massif-press/lancer-data)
- Built for the [Lancer TTRPG](https://massif-press.itch.io/corebook-pdf) by Massif Press

