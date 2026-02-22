# Backend Tests

## MCP Server Test API

A FastAPI-based test API to verify MCP server connectivity to PostgreSQL.

### Files

- **test_api.py**: FastAPI application exposing MCP server functions as REST endpoints
- **run_test_api.py**: Runner script in project root

### Running Tests

#### Option 1: From project root
```bash
python run_test_api.py --port 8000
```

#### Option 2: From backend/tests directory
```bash
cd backend/tests
python test_api.py
```

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/test-connection` | Test database connectivity |
| GET | `/schemas` | List all schemas |
| GET | `/tables/{schema_name}` | List tables in schema |
| GET | `/table-details/{schema_name}/{table_name}` | Get table structure |
| GET | `/statistical-sample/{schema_name}/{table_name}` | Get column statistics |
| POST | `/sql-query` | Execute SELECT query |

### Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Environment Variables

Required in `.env`:
```
DB_HOST=localhost
DB_PORT=5433
DB_USER=hackfest
DB_PASSWORD=hackfest
DB_NAME=hackfest_db

# API Authentication (optional, defaults shown)
API_USERNAME=admin
API_PASSWORD=password123
```

## Authentication

All endpoints (except root `/`) require **HTTP Basic Authentication**.

**Default Credentials:**
- Username: `admin`
- Password: `password123`

### In Postman

1. Go to **Authorization** tab
2. Select **Basic Auth**
3. Enter:
   - Username: `admin`
   - Password: `password123`
4. Send request

### Import Postman Collection

1. Download `MCP_Server_Test_API.postman_collection.json` from `/backend/tests/`
2. Open Postman → **Import**
3. Select the JSON file
4. All requests are pre-configured with authentication
5. Update variables in collection:
   - `{{base_url}}`: `http://localhost:8000`
   - `{{api_username}}`: `admin`
   - `{{api_password}}`: `password123`
   - `{{schema_name}}`: `public` (change as needed)
   - `{{table_name}}`: your table name

### Basic Test Examples

**With cURL (Basic Auth):**
```bash
# Test connection
curl -u admin:password123 http://localhost:8000/test-connection

# List schemas
curl -u admin:password123 http://localhost:8000/schemas

# Get tables from a schema
curl -u admin:password123 http://localhost:8000/tables/public

# Get table details
curl -u admin:password123 http://localhost:8000/table-details/public/users

# Get statistics
curl -u admin:password123 http://localhost:8000/statistical-sample/public/users

# Run SQL query (POST)
curl -u admin:password123 -X POST http://localhost:8000/sql-query \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM public.users LIMIT 10"}'
```

**Custom Credentials (override in .env):**
```bash
curl -u your_username:your_password http://localhost:8000/schemas
```

### Pytest Files

Place your Pytest test files here.
Example: `test_adapters.py`
