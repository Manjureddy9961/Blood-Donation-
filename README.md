# Rakthdhaan - Blood Donation Management System

A comprehensive web-based application built with Django to manage blood donations, donor tracking, and camp management securely.

## Overview
Rakthdhaan allows administrators and donors to keep a streamlined track of blood donations. It features modern technologies such as:
- **QR Code Tracking**: Generates verifiable QR codes upon successful donations.
- **Blockchain Integration**: Securely tracks and logs data to a blockchain ecosystem.
- **Dashboard Management**: Dedicated dashboards for users and administrators.

## Technologies Used
- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (Local) / PostgreSQL (Production)
- **Web3**: Blockchain integration for data integrity

## Getting Started Locally

### Prerequisites
- Python 3.x installed
- pip (Python package installer)

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/Manjureddy9961/Blood-Donation-.git
   cd Blood-Donation-
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations to set up the database:
   ```bash
   python manage.py migrate
   ```
4. Start the local server:
   ```bash
   python manage.py runserver
   ```
5. Open `http://127.0.0.1:8000/` in your web browser.
