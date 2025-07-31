# 🚀 AI-mVISE Deployment Guide

## 📁 **Repository Structure**
```
Ai-mVISE/
├── backend/           # FastAPI + Amazon Bedrock
├── frontend/          # Next.js + TypeScript
├── .gitignore        # Comprehensive ignore rules
├── README.md         # Main documentation
├── setup.sh          # Automated setup script
└── package.json      # Root package configuration
```

## 🔧 **Prerequisites**

### **System Requirements**
- **Node.js** >= 18.0.0
- **Python** >= 3.8
- **Git** (latest version)
- **AWS Account** with Bedrock access

### **AWS Setup Required**
1. **Amazon Bedrock Access**
   - Enable Claude 3.5 Sonnet model
   - Region: `us-east-1` (recommended)
   - IAM permissions for `bedrock:InvokeModel`

2. **AWS Credentials**
   - Access Key ID
   - Secret Access Key
   - Region configuration

## 🚀 **Local Development Setup**

### **Quick Start**
```bash
# 1. Clone repository
git clone https://github.com/ahmadasakra/aimvise.git
cd aimvise

# 2. Run automated setup
chmod +x setup.sh
./setup.sh

# 3. Configure AWS credentials
cd backend
cp .env.example .env
# Edit .env with your AWS credentials

# 4. Start development servers
npm run dev
```

### **Manual Setup**
```bash
# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend setup  
cd ../frontend
npm install

# Root dependencies
cd ..
npm install
```

## 🌍 **Production Deployment Options**

### **Option 1: Vercel (Frontend) + Railway/Render (Backend)**

#### **Frontend (Vercel)**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy frontend
cd frontend
vercel --prod

# Set environment variables in Vercel dashboard:
# NEXT_PUBLIC_API_URL=https://your-backend-url.com/api
```

#### **Backend (Railway)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway add --service postgres  # Optional database
railway deploy

# Set environment variables:
# AWS_REGION=us-east-1
# AWS_ACCESS_KEY_ID=your_key
# AWS_SECRET_ACCESS_KEY=your_secret
```

### **Option 2: Docker Deployment**

#### **Backend Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### **Frontend Dockerfile**
```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --only=production

COPY frontend/ .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

#### **Docker Compose**
```yaml
version: '3.8'
services:
  backend:
    build: 
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - AWS_REGION=${AWS_REGION}
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
    
  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000/api
    depends_on:
      - backend
```

### **Option 3: AWS Deployment**

#### **Backend (AWS Lambda + API Gateway)**
```bash
# Install Serverless Framework
npm install -g serverless
npm install serverless-python-requirements

# Create serverless.yml in backend/
serverless deploy --stage prod
```

#### **Frontend (AWS Amplify)**
```bash
# Install Amplify CLI
npm install -g @aws-amplify/cli

# Initialize and deploy
amplify init
amplify add hosting
amplify publish
```

## 🔐 **Environment Configuration**

### **Backend (.env)**
```bash
# AWS Bedrock Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...

# Application Settings
DEBUG=false
LOG_LEVEL=INFO
CORS_ORIGINS=https://your-frontend-domain.com

# Optional: Database (for persistent storage)
DATABASE_URL=postgresql://user:pass@localhost/aimvise

# Optional: Redis (for caching)
REDIS_URL=redis://localhost:6379/0
```

### **Frontend (.env.local)**
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.com/api
NEXT_PUBLIC_APP_NAME=AI-mVISE Repository Analyzer
NEXT_PUBLIC_ENABLE_ANALYTICS=false
```

## 📊 **Monitoring & Analytics**

### **Backend Monitoring**
- **Health Check**: `GET /api/health`
- **Metrics**: Analysis completion rates
- **Logging**: Structured JSON logs
- **Error Tracking**: Sentry integration (optional)

### **Performance Optimization**
- **Caching**: Redis for analysis results
- **CDN**: Static assets via CloudFront/Vercel
- **Database**: Connection pooling
- **Rate Limiting**: API request throttling

## 🛡️ **Security Considerations**

### **Production Security**
```bash
# Environment variables (never commit)
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- SECRET_KEY
- DATABASE_URL

# Security headers
- CORS configuration
- Rate limiting
- Input validation
- SQL injection prevention
```

### **AWS Security**
- **IAM Roles**: Minimal permissions
- **VPC**: Network isolation (optional)
- **Secrets Manager**: Credential management
- **CloudTrail**: API call logging

## 🔄 **CI/CD Pipeline**

### **GitHub Actions Example**
```yaml
name: Deploy AI-mVISE
on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: |
          cd backend
          pip install -r requirements.txt
          # Run tests
          # Deploy to production
          
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: |
          cd frontend
          npm ci
          npm run build
          # Deploy to Vercel/Netlify/AWS
```

## 🆘 **Troubleshooting**

### **Common Issues**
1. **AWS Bedrock Access Denied**
   - Check IAM permissions
   - Verify model access in Bedrock console
   - Confirm region (us-east-1)

2. **CORS Issues**
   - Update CORS_ORIGINS in backend
   - Check frontend API URL configuration

3. **Memory Issues**
   - Increase server memory limits
   - Optimize repository cloning size limits

### **Health Checks**
```bash
# Backend health
curl https://your-backend-url.com/api/health

# Frontend health  
curl https://your-frontend-url.com/

# AWS connectivity
aws bedrock list-foundation-models --region us-east-1
```

## 📈 **Scaling Considerations**

### **Performance Optimization**
- **Background Tasks**: Celery/Redis for analysis queue
- **Database**: PostgreSQL with connection pooling
- **Caching**: Redis for frequently accessed data
- **CDN**: Static asset delivery optimization

### **Cost Optimization**
- **AWS Bedrock**: Monitor token usage
- **Serverless**: Pay-per-request pricing
- **Caching**: Reduce redundant API calls
- **Resource Limits**: Set analysis timeouts

## 📞 **Support & Maintenance**

### **Monitoring Dashboard**
- Application metrics
- Error rates and logs  
- AWS Bedrock usage costs
- User analytics

### **Backup Strategy**
- Database backups
- Configuration backups
- Source code version control
- Environment documentation

---

## 🎯 **Quick Deployment Commands**

```bash
# Production deployment checklist
□ AWS credentials configured
□ Environment variables set
□ Dependencies installed
□ Tests passing
□ Security review completed
□ Monitoring configured

# Deploy commands
npm run build          # Build frontend
npm run deploy:backend # Deploy backend
npm run deploy:frontend # Deploy frontend
npm run health-check   # Verify deployment
```

**🚀 Your AI-mVISE platform is now ready for production!** 