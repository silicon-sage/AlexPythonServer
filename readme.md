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

### Installation
```bash
# Clone the repository
git clone https://github.com/silicon-sage/AlexPythonServer

# Install dependencies
pip install -r requirements.txt

# Start the development server
py run.py
```

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
- User session and authentication. Right now all users share the same token, this should be improved and the user should only be able to edit and see their own records. In the document it says to exclude security
- File upload capability for actual medical documents (PDFs, images)
- Integration with healthcare providers' systems
- Enhanced security features for HIPAA compliance
- Mobile application support
- Export functionality for sharing records with healthcare providers
- Data visualization for tracking health metrics over time

## License
[MIT](https://choosealicense.com/licenses/mit/)