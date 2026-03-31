# SafeGuard AI: Women Safety and Emergency Response System

SafeGuard AI is a full-stack Python Flask application designed to provide immediate assistance to women in distress. It leverages Machine Learning (Natural Language Processing) to classify the nature of an emergency based on user input and alerts regional volunteers and family members instantly.

## Features

- **Multi-Role Authentication**: Secure login and registration for Users, Volunteers, and Administrators.
- **AI Classification**: Uses a Naive Bayes classifier to categorize emergencies into Medical, Accident, Fire, Crime, or Others.
- **Region-Based Volunteer System**: SOS alerts are routed specifically to volunteers within the same geographic region for faster response times.
- **One-Touch SOS**: A prominent emergency button that logs events, notifies family, and signals responders.
- **Helpline Directory**: Direct access to local emergency services (Police, Ambulance, Fire).
- **Admin Analytics**: Real-time data visualization of emergency trends and regional hotspots using Chart.js.
- **Persistent Logging**: Complete database of all emergency events, their status (Pending/Resolved), and responder actions.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone or download this project.
2. Navigate to the project root directory.
3. Install the required dependencies:
    `pip install -r requirements.txt`

## How to Run

1. Execute the application:
    `python app.py`
2. The server will start locally at: `http://127.0.0.1:5000`
3. The database (`safety_system.db`) will be automatically created on first run.

## Default Credentials

For testing purposes, a default administrative account is automatically created:
- **Username**: `admin`
- **Password**: `admin123`

## Usage Guide

1. **Individual User**:
   - Register choosing the 'Individual User' role.
   - Access the dashboard to see the SOS button.
   - Describe your situation (e.g., "Someone is following me") and press SOS.
   - The AI will classify it as 'Crime'.

2. **Volunteer**:
   - Register choosing the 'Volunteer' role.
   - Ensure your region matches the user's region to receive alerts.
   - View pending alerts in your specific region and mark them as 'Resolved' once help is provided.

3. **Administrator**:
   - Log in with default credentials.
   - View global statistics on emergency types and regional activity.

## Project Structure

- `app.py`: Main Flask server, routes, and business logic.
- `models.py`: Database schema definitions (User, EmergencyLog).
- `ml_engine.py`: Scikit-learn NLP model for text classification.
- `templates/`: HTML interface templates (Bootstrap 5).
- `static/`: CSS styling and JavaScript for Chart.js.

## Troubleshooting

- **Chart not loading**: Ensure you are logged in as an administrator.
- **Database errors**: If the database schema changes, delete `safety_system.db` and restart the app to recreate it.
- **Role Redirection**: Role-based access is strictly enforced; ensure you select the correct role during registration to access specific dashboards.
