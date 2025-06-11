# NextJob AI

NextJob AI is an intelligent platform designed to streamline job searching and recruitment using AI-powered tools. It features a modern web backend (Django), a mobile app (React Native/Expo), and various microservices for enhanced automation and integration.

---

## Features

- **AI-Powered Job Matching:** Get personalized job recommendations using advanced AI algorithms.
- **Job Offer Management:** Easily create, edit, and manage job offers.
- **Mobile App:** Access job listings and apply on the go with the NextJob AI mobile app.
- **Microservices Architecture:** Modular services for scalability and maintainability.
- **Secure & Scalable:** Built with best practices for security and performance.

---

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Frontend:** React Native (Expo)
- **Microservices:** Python
- **Database:** Sqlite3
- **AI Integration:** OpenAI API
- **DevOps:** Docker, GitHub Actions
- **Python Environment:** Pipenv

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/nextjob-ai.git
cd nextjob-ai
```

### 2. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your environment variables
python manage.py migrate
python manage.py runserver
```

### 3. Mobile App Setup

```bash
cd ../nextjob-ai
npm install
cp .env.example .env  # Add your environment variables
npx expo start
```

### 4. Microservices Setup

```bash
cd ../services/digest_generator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys and configs
```

---

## Environment Variables

- Each service/app uses a `.env` file for configuration.
- See `.env.example` in each folder for required variables.

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or support, please open an issue or contact [igorvgalas@gmail.com](mailto:igorvgalas@gmail.com).

---
