# Personal Health Record App

## Overview
My Health Diary is a web-based solution designed to help people with chronic diseases maintain and organize their medical records effectively. Unlike traditional file storage solutions like Dropbox, my application provides a structured, chronological view of medical documents with enhanced organization capabilities.

The app enables patients to maintain a comprehensive timeline of their healthcare journey, making it easier to share their medical history with new specialists and ensure continuity of care. Users can easily categorize, search, and review their medical documents based on type, date, provider, and other relevant criteria.

## Features
- **Chronological Timeline**: View all medical records in a descending date order for easy access to recent and historical data
- **Smart Document Classification**: Organize records into distinct categories:
  - Lab Results (numerical values with descriptions)
  - Prescriptions (dosage and medication details)
  - Appointment Note (free-text format)
  - Self-Measurements (patient-recorded metrics)
- **Quick Record Entry**: Simple form interface for adding new medical records with automatic categorization
- **Record Organization**: Filter and sort capabilities by document type, date, and healthcare provider
- **Data Preview**: Instant preview of record contents without opening full details

## Technology Stack
- Frontend: Vanilla JavaScript, HTML5
- Backend: Python Flask Server
- Database: Redis

## Getting Started

### Prerequisites
```bash
python >= 13.0
```

# Installation Guide

## Required: Redis Setup (Do this first)
You must set up Redis before deploying the application, regardless of which deployment method you choose.

### Option A: Using Docker for Redis (Recommended)
```bash
# Pull and run Redis container
docker pull redis
docker run --name alex-redis -p 6379:6379 -d redis
```

### Option B: Local Redis Installation
#### For Ubuntu/Debian:
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

#### For macOS:
```bash
brew install redis
brew services start redis
```

#### For Windows:
Download and install from [Redis Windows Downloads](https://github.com/microsoftarchive/redis/releases)

## Application Deployment Options

## Configuration
Make sure to update config.json with your Redis connection details:
```json
{
  "redis": {
    "host": "localhost",
    "port": 6379,
    "db": 0
  }
}
```

### Option 1: Using Docker
```bash
# Clone the repository
git clone https://github.com/silicon-sage/AlexPythonServer

# Navigate to project directory
cd AlexPythonServer

# Build the Docker image
docker build -t flask-server .

# Run the container
docker run -d --name flask-server -p 5000:5000 flask-server

# Don't forget to update config.json with your Redis connection details!
```

### Option 2: Manual Debug Server Installation
```bash
# Clone the repository
git clone https://github.com/silicon-sage/AlexPythonServer

# Navigate to project directory
cd AlexPythonServer

# Install dependencies
pip install -r requirements.txt

# Start the development server
py run.py
```

## Verification
To verify the installation:
1. Check if Redis is running:
   ```bash
   redis-cli ping
   ```
   Should return "PONG"

2. The application should be running at http://localhost:5000 (or your configured port)

## Troubleshooting
- If Redis connection fails, verify Redis is running and the config.json settings match your Redis installation
- For Docker users:
  - Check if containers are running: `docker ps`
  - View application logs: `docker logs flask-server`
  - View Redis logs: `docker logs alex-redis`
- For local installation:
  - Check Redis logs in system logs or Redis log file
  - Verify Python dependencies are installed correctly
### Running Tests
```bash
pytest
```

## Usage

### Adding a New Record
```javascript
// Example of adding a new lab result
let data = {
    type: type,
    provider: self_recorded,
    patient_id: "123",
	value = 10,
	description = "Blood Sugar"
};

fetch('/health-records', {
	method: 'POST',
	headers: {
		'Content-Type': 'application/json',
	},
	body: JSON.stringify(data)
})
```

## Record Types
The application supports four types of medical records, each inheriting from a base HealthRecord class:

### Base Record Structure
All records contain these base fields:
```python
{
    "id": str,  # UUID4
    "type": str,  # Record type identifier
    "patient_id": str,
    "provider": str | None,
    "timestamp": str  # ISO format datetime
}
```

### 1. Lab Results
```python
{
    **base_fields,
    "value": float,
    "description": str
}
```

### 2. Prescriptions
```python
{
    **base_fields,
    "dose": str,
    "drug": str
}
```

### 3. Appointment Notes
```python
{
    **base_fields,
    "note": str
}
```

### 4. Self-Measurements
```python
{
    **base_fields,
    "value": float,
    "description": str
}
```

## Usage Examples

### Creating Records
```python
# Lab Result
lab_result = LabResult(
    patient_id="123",
    value=100.0,
    description="Cholesterol",
    provider="Dr. Smith"
)

# Prescription
prescription = Prescription(
    patient_id="123",
    dose="100mg",
    drug="Aspirin",
    provider="Dr. Johnson"
)

# Appointment Note
appointment = AppointmentNote(
    patient_id="123",
    note="Patient reported feeling better",
    provider="Dr. Brown"
)

# Self-Measurement
measurement = SelfMeasurement(
    patient_id="123",
    value=8.9,
    description="blood sugar"
)
```

## Project Structure
```
.
├── app/
│   ├── models/          # Data models and record types
│   ├── routes/          # API endpoints and route handlers
│   ├── services/        # Business logic and data processing
│   └── templates/       # HTML templates
└── tests/               # Test suite
```

## Design Decisions
- **Document-Based Database**: Chose redis for flexible schema design and natural handling of different record types
- **Timeline-First Approach**: Prioritized chronological view as well as the data filtering as the main interface based on user needs

## Future Improvements
- User session and authentication. Right now all users share the same token, this should be improved and the user should only be able to edit and see their own records. In the document it says to exclude security, so this feature was not prioritzed
- File upload capability for actual medical documents (PDFs, images)
- Integration with healthcare providers' systems
- Enhanced security features for HIPAA compliance
- Mobile application support, the website works on mobile but the ease of use can be improved
- Export functionality for sharing records with healthcare providers
- Data visualization for tracking health metrics over time
- Performance under load. Current implementation is using Redis which will require all information to be stored in memory, also some filtering is done in memory with O(n) speed

## Error Handling
The application implements basic error handling:

1. Database Errors
   - All Redis errors are logged
   - Automatic reconnection attempts
   - Errors are reported back to the client appropriately
2. API Errors
   - Standard error response format
   - Error logging for debugging
3. Input Validation
   - Request payload validation

## License
[MIT](https://choosealicense.com/licenses/mit/)