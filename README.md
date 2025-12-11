# NextJob AI

NextJob AI is an intelligent platform designed to streamline job searching and recruitment using AI-powered tools. It features a modern FastAPI backend and a mobile app (React Native/Expo). Legacy standalone microservices have been retired in favor of the simplified architecture v2 documented in `ARCHITECTURE.md`.

---

## Features

- **AI-Powered Job Matching:** Get personalized job recommendations using advanced AI algorithms.
- **Job Offer Management:** Easily create, edit, and manage job offers.
- **Mobile App:** Access job listings and apply on the go with the NextJob AI mobile app.
- **Background Integrations:** Gmail/LinkedIn ingestion and LLM-powered analysis run through backend integrations and workers.
- **Secure & Scalable:** Built with best practices for security and performance.

---

## Tech Stack

- **Backend:** FastAPI
- **Frontend:** React Native (Expo)
- **Workers/Integrations:** Python helpers invoked from the backend
- **Database:** PostgreSQL
- **AI Integration:** OpenAI API
- **DevOps:** Docker, GitHub Actions
- **Python Environment:** venv

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
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. Mobile App Setup

```bash
cd ../nextjob-ai
npm install
cp .env.example .env  # Add your environment variables
npx expo start
```

---

## Environment Variables

- Each app uses a `.env` file for configuration.
- See `.env.example` in the relevant folder for required variables.

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
