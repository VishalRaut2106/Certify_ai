# 🎓 AI-Powered Bulk Certificate Verification System

A comprehensive solution for educational institutes to automatically verify certificate authenticity at scale using AI-powered fraud detection.

## 🚀 Features

- **Bulk Certificate Upload** - Process up to 100 certificates simultaneously
- **Multi-Layer AI Verification** - OCR, Computer Vision, Template Matching, Fraud Detection
- **Real-time Processing** - WebSocket-based progress tracking
- **Trust Scoring** - 0-100 confidence scores with detailed reasoning
- **Fraud Detection** - Advanced algorithms to detect fake certificates
- **Platform Integration** - Verify with Coursera, edX, and other platforms
- **ERP Integration** - REST APIs for college management systems
- **Responsive Dashboard** - Modern React/Next.js interface

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **MongoDB Atlas** - Cloud database (512MB free tier)
- **Redis** - Caching and session management
- **Cloudinary** - File storage and processing (10GB free)

### AI/ML Components
- **OpenCV** - Computer vision and template matching
- **Tesseract OCR** - Multi-language text extraction
- **scikit-learn** - Machine learning fraud detection
- **fuzzywuzzy** - Fuzzy name matching

### Frontend
- **Next.js 14** - React framework with TypeScript
- **Tailwind CSS** - Utility-first CSS framework
- **React Query** - Data fetching and state management
- **Socket.io** - Real-time communication

### Deployment
- **Railway** - Backend hosting (free tier)
- **Vercel** - Frontend hosting (free tier)
- **Docker** - Containerization

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB Atlas account
- Cloudinary account
- Railway account
- Vercel account

## 🔧 Environment Variables

Create a `.env` file in the backend directory:

```bash
# Database
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/certificate_verification

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Authentication
JWT_SECRET_KEY=your_super_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# Application
ENVIRONMENT=development
DEBUG=True
PORT=8000
```

## 🚀 Quick Start

### Backend Setup

1. **Clone and navigate to backend**
   ```bash
   cd certificate-verification-system/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

   API will be available at: http://localhost:8000
   Documentation: http://localhost:8000/docs

### Frontend Setup

1. **Navigate to frontend**
   ```bash
   cd certificate-verification-system/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   # Create .env.local
   NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
   NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
   ```

4. **Run the development server**
   ```bash
   npm run dev
   ```

   Frontend will be available at: http://localhost:3000

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user

### Upload
- `POST /api/v1/upload/single` - Upload single certificate
- `POST /api/v1/upload/bulk` - Upload multiple certificates
- `GET /api/v1/upload/batch/{batch_id}/progress` - Get batch progress

### Certificates
- `GET /api/v1/certificates` - List user certificates
- `GET /api/v1/certificates/{id}` - Get certificate details
- `DELETE /api/v1/certificates/{id}` - Delete certificate

### Verification
- `GET /api/v1/verification/results` - Get verification results
- `POST /api/v1/verification/manual-review` - Manual review
- `GET /api/v1/verification/statistics` - Get statistics

## 🔒 Security Features

- **JWT Authentication** - Secure token-based authentication
- **Role-based Access Control** - Admin, Teacher, Evaluator roles
- **File Validation** - MIME type and content validation
- **Rate Limiting** - API request throttling
- **Data Encryption** - AES-256 encryption for sensitive data
- **Audit Logging** - Complete activity tracking

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm run test
```

### Property-Based Testing
```bash
cd backend
pytest tests/property_tests/ -v --hypothesis-show-statistics
```

## 🚀 Deployment

### Backend (Railway)

1. **Connect GitHub repository to Railway**
2. **Set environment variables in Railway dashboard**
3. **Deploy automatically on git push**

### Frontend (Vercel)

1. **Connect GitHub repository to Vercel**
2. **Set environment variables in Vercel dashboard**
3. **Deploy automatically on git push**

## 📈 Performance

- **Processing Time**: <30 seconds per certificate
- **Concurrent Processing**: Up to 100 certificates
- **Uptime**: 99.5% availability target
- **Scalability**: Horizontal scaling support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [API Docs](http://localhost:8000/docs)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Email**: support@certificateverification.com

## 🎯 Roadmap

- [ ] Mobile app development
- [ ] Advanced ML models
- [ ] Blockchain integration
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Third-party integrations

---

**Built with ❤️ for educational institutions worldwide**
