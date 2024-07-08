# ProblemBuddy

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)![Version](https://img.shields.io/badge/version-1.0 -blue)
![License](https://img.shields.io/badge/license-MIT-green)

Welcome to ProblemBuddy. Your personal problem recommendor.We recommend problems by analyzing your track record and other succesfull people's track record.
## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

”Problembuddy” is a web-based application tailored exclusively for Codeforces users who
are competitive programmers. The system operates through three phases: Register, Train and Recommendation. In the Registration Phase, users provide their Codeforces handles, allowing data retrieval from the Codeforces API. Users then input their handles to identify current skills, target rank, and weak areas. Using vectors and cosine similarity, the Recommendation Phase suggests problems that align with users abilities. The Train phase allows users to train the system with the data of their favorite coder's track record.

## Installation

To set up Competitive Programming Progress Tracker locally, follow these steps:

1. Clone the repository: `git clone https://github.com/Mehedi-10/Competitive-Programming-Progress-Tracker.git`
2. Navigate to the project directory: `cd Competitive-Programming-Progress-Tracker`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate the virtual environment:
   - On macOS and Linux: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Apply migrations: `python manage.py migrate`
7. Create a superuser account: `python manage.py createsuperuser`
8. Start the development server: `python manage.py runserver`

## Usage

After starting the development server, open your web browser and go to `http://localhost:8000`. You can create an account, log in, and begin tracking your daily programming activities. The user-friendly interface lets you visualize your progress over time and receive personalized feedback from experienced coaches.

## Features

- Get problems
- Know your weak points
- Train data

## Contributing

Contributions to Competitive Programming Progress Tracker are welcomed! To contribute:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request

For significant changes, please open an issue first to discuss the proposed changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

Have questions or suggestions? Feel free to contact me at `rakibhjoy@gmail.com`.
