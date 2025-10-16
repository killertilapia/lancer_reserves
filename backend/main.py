import json
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import strawberry
from strawberry.fastapi import GraphQLRouter

from backend.database import init_db, get_db, SessionLocal
from backend.api.v1 import api_router
from backend.graphql.queries import Query
from backend.graphql.mutations import Mutation
from backend.models.reserves import Reserve


def seed_database():
    """Seed database with data from reserves.json if it exists and database is empty"""
    reserves_file = Path("reserves.json")
    if not reserves_file.exists():
        print("No reserves.json file found. Skipping seed.")
        return
    
    db = SessionLocal()
    try:
        # Check if database already has data
        count = db.query(Reserve).count()
        if count > 0:
            print(f"Database already contains {count} reserves. Skipping seed.")
            return
        
        # Load and seed data
        with open(reserves_file, "r", encoding="utf-8") as f:
            reserves_data = json.load(f)
        
        for reserve_dict in reserves_data:
            db_reserve = Reserve(
                id=reserve_dict["id"],
                name=reserve_dict["name"],
                type=reserve_dict["type"],
                label=reserve_dict["label"],
                description=reserve_dict["description"],
                bonuses=reserve_dict.get("bonuses"),
                deployables=reserve_dict.get("deployables"),
                actions=reserve_dict.get("actions"),
                synergies=reserve_dict.get("synergies"),
            )
            db.add(db_reserve)
        
        db.commit()
        print(f"Successfully seeded database with {len(reserves_data)} reserves from reserves.json")
    
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for FastAPI application"""
    # Startup
    print("Initializing database...")
    init_db()
    print("Seeding database...")
    seed_database()
    yield
    # Shutdown
    print("Application shutting down...")


# Create FastAPI application
app = FastAPI(
    title="Lancer Reserves API",
    description="REST and GraphQL API for managing Lancer TTRPG reserves",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include REST API routes
app.include_router(api_router, prefix="/api/v1")

# Configure GraphQL
schema = strawberry.Schema(query=Query, mutation=Mutation)


async def get_context():
    """Provide context for GraphQL requests"""
    db = SessionLocal()
    try:
        yield {"db": db}
    finally:
        db.close()


graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

app.include_router(graphql_app, prefix="/graphql", tags=["graphql"])


@app.get("/", tags=["root"])
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Lancer Reserves API",
        "version": "1.0.0",
        "endpoints": {
            "rest_api": "/api/v1/reserves",
            "graphql": "/graphql",
            "documentation": "/docs",
            "redoc": "/redoc",
        }
    }


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



