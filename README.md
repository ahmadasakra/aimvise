# AI-mVISE Repository Analyzer 🚀

Ein **AI-gestütztes Repository-Analyse-System** mit Amazon Bedrock Claude für **umfassende Code-Bewertung** und **Business-Intelligence**.

## 🎯 **Features**

### **🧠 AI-Powered Analysis (Amazon Bedrock Claude 3.5 Sonnet)**
- **Architektur-Pattern-Erkennung** (MVC, Microservices, etc.)
- **Code-Qualitäts-Bewertung** mit KI-Insights
- **Security-Risk-Assessment** mit Vulnerability-Scanning
- **Business-Impact-Analyse** und Investment-Empfehlungen
- **Executive-Summary** für Management

### **🔧 Static Code Analysis**
- **Complexity Analysis** (Radon - Cyclomatic Complexity)
- **Security Scanning** (Bandit - Python Security Issues)
- **Code Quality** (PyLint - Style & Quality Issues)
- **Dependency Analysis** (Outdated Packages, Vulnerabilities)

### **📊 Comprehensive Reporting**
- **1-100 Qualitäts-Skala** (Industry Standards)
- **Technical Debt** Bewertung in Stunden
- **ROI-Kalkulation** für Code-Verbesserungen
- **Prioritäts-Roadmap** für Entwicklung

## 🏗️ **System-Architektur**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React         │    │   FastAPI       │    │   Amazon        │
│   Frontend      │    │   Backend       │    │   Bedrock       │
│                 │    │                 │    │                 │
│ • Modern UI     │───▶│ • Git Cloning   │───▶│ • Claude 3.5    │
│ • Real-time     │    │ • Static Tools  │    │ • AI Analysis   │
│ • Reports       │◀───│ • Orchestration │◀───│ • Deep Insights │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │
                       ┌─────────────────┐
                       │   Analysis      │
                       │   Tools         │
                       │                 │
                       │ • Radon         │
                       │ • Bandit        │
                       │ • PyLint        │
                       │ • Git Tools     │
                       └─────────────────┘
```

## 🚀 **Installation & Setup**

### **1. Repository Setup**
```bash
git clone <your-repo>
cd Ai-mVISE
```

### **2. Backend Setup (Python + Amazon Bedrock)**

#### **2.1 Python Virtual Environment**
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### **2.2 AWS Bedrock Configuration** 🔑

**Option A: AWS CLI (Empfohlen)**
```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure
# AWS Access Key ID: [Your Access Key]
# AWS Secret Access Key: [Your Secret Key]  
# Default region name: us-east-1
# Default output format: json
```

**Option B: Environment Variables**
```bash
# Create .env file in backend directory
cd backend
cat > .env << EOF
# AWS Bedrock Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here

# Optional GitHub Token
GITHUB_TOKEN=your_github_token_here

# FastAPI Configuration  
DEBUG=true
LOG_LEVEL=INFO
EOF
```

#### **2.3 Analysis Tools Installation**
```bash
# Code analysis tools (bereits in requirements.txt)
pip install radon bandit pylint flake8 mypy safety

# Git (system requirement)
# macOS: brew install git
# Ubuntu: sudo apt install git
# Windows: Download from git-scm.com
```

### **3. Frontend Setup (React/Next.js)**
```bash
cd frontend

# Install dependencies
npm install

# Development server
npm run dev
```

### **4. Complete System Start**
```bash
# From project root directory
npm run dev
```
Dies startet:
- **Backend**: `http://localhost:8000` (FastAPI + Bedrock)
- **Frontend**: `http://localhost:3000` (React)

## 🔑 **AWS Bedrock Setup (Critical!)**

### **Amazon Bedrock Zugriff aktivieren**

1. **AWS Console** → **Amazon Bedrock**
2. **Model Access** → **Enable Access**
3. **Claude 3.5 Sonnet** aktivieren
4. **Region**: `us-east-1` (empfohlen)

### **IAM Permissions**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0"
            ]
        }
    ]
}
```

### **Bedrock Model Testing**
```bash
# Test Bedrock connection
cd backend
python -c "
import boto3
try:
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    print('✅ AWS Bedrock connection successful')
except Exception as e:
    print(f'❌ Connection failed: {e}')
"
```

## 📋 **Usage**

### **1. Repository Analysis starten**
1. **Frontend** öffnen: `http://localhost:3000`
2. **"Repository Analyzer"** klicken
3. **Repository URL** eingeben (z.B. `https://github.com/user/repo`)
4. **GitHub Token** (optional, für private repos)
5. **Analysis Type** wählen:
   - **Quick**: Basis-Analyse (5 min)
   - **Standard**: Erweiterte Analyse (15 min)
   - **Comprehensive**: Vollständige AI-Analyse (30 min)

### **2. Real-time Progress**
- **Live Progress** mit aktueller Stage
- **Fortschritts-Balken** (0-100%)
- **ETA** und Status-Updates

### **3. Analyse-Ergebnisse**
- **Executive Summary** (Management-ready)
- **Technical Scores** (1-100 Skala)
- **AI Insights** (Architektur, Empfehlungen)
- **Investment Roadmap** (Prioritäten, ROI)

## 🔍 **Analysis Pipeline**

### **Stage 1: Repository Cloning (10%)**
- Git Repository klonen
- Metadaten extrahieren
- File-System scannen

### **Stage 2: File Analysis (25%)**
- Code-Files identifizieren
- Programmiersprachen erkennen
- Lines of Code zählen

### **Stage 3: Static Analysis (40%)**
- **Radon**: Complexity Metrics
- **Bandit**: Security Vulnerabilities
- **PyLint**: Code Quality Issues
- **Dependency**: Outdated Packages

### **Stage 4: AI Architecture Analysis (55%)**
- **Claude 3.5 Sonnet** analysiert Code-Struktur
- **Pattern Recognition** (MVC, Clean Architecture)
- **Design Quality** Assessment
- **Scalability** Evaluation

### **Stage 5: AI Quality Analysis (70%)**
- **Code Readability** Bewertung
- **Maintainability** Score
- **Performance** Issues
- **Refactoring** Suggestions

### **Stage 6: AI Security Analysis (85%)**
- **Security Risks** Assessment
- **Vulnerability** Impact Analysis
- **Compliance** Check (GDPR, etc.)
- **Security** Recommendations

### **Stage 7: Report Generation (95%)**
- **Executive Summary** generieren
- **Business Impact** kalkulieren
- **Investment Recommendations** priorisieren
- **Industry Comparison** durchführen

### **Stage 8: Finalization (100%)**
- **Comprehensive Report** fertigstellen
- **Cleanup** temporärer Files
- **Results** bereitstellen

## 📊 **Example Analysis Output**

```json
{
  "repository_overview": {
    "name": "my-awesome-app",
    "languages": ["Python", "JavaScript", "TypeScript"],
    "lines_of_code": 45230,
    "total_files": 187
  },
  "overall_scores": {
    "overall_quality_score": 87,
    "architecture_score": 92,
    "security_score": 78,
    "maintainability_score": 85
  },
  "ai_insights": {
    "architecture_pattern": "Clean Architecture with DDD",
    "strengths": [
      "Klare Service-Trennung",
      "Gute Abstraktions-Schichten",
      "Solid SOLID-Prinzipien"
    ],
    "recommendations": [
      "Dependency Injection implementieren",
      "Unit Test Coverage erhöhen",
      "API Rate Limiting hinzufügen"
    ]
  },
  "business_impact": {
    "technical_debt_hours": 120,
    "development_velocity": "medium",
    "maintenance_cost": "low"
  },
  "investment_recommendations": [
    {
      "priority": 1,
      "task": "Security Fixes",
      "effort_hours": 40,
      "business_value": "high"
    }
  ]
}
```

## 🛠️ **API Endpoints**

### **Analysis Endpoints**
- `POST /api/analysis/start` - Start analysis
- `GET /api/analysis/{id}/progress` - Get progress
- `GET /api/analysis/{id}` - Get results
- `DELETE /api/analysis/{id}` - Delete analysis

### **Management Endpoints**
- `GET /api/analysis` - List all analyses
- `GET /api/dashboard/stats` - Platform statistics
- `GET /api/health` - Health check

## 🔧 **Troubleshooting**

### **Common Issues**

#### **❌ "Analysis service not available"**
```bash
# Check AWS credentials
aws sts get-caller-identity

# Check Bedrock access
aws bedrock list-foundation-models --region us-east-1
```

#### **❌ "Git clone failed"**
- Repository URL korrekt?
- GitHub Token für private repos?
- Internet-Verbindung verfügbar?

#### **❌ "Static analysis tools missing"**
```bash
# Re-install analysis tools
pip install radon bandit pylint flake8 mypy
```

#### **❌ "Bedrock model access denied"**
- **Amazon Bedrock Console** → **Model Access** prüfen
- **IAM Permissions** für Bedrock prüfen
- **Region** (us-east-1) korrekt?

### **Logs & Debugging**
```bash
# Backend logs
cd backend
python -m uvicorn app.main:app --reload --log-level debug

# Frontend logs
cd frontend  
npm run dev

# AWS CLI debug
aws bedrock list-foundation-models --region us-east-1 --debug
```

## 🎯 **Best Practices**

### **Repository Selection**
- **Public Repos**: Keine Token erforderlich
- **Private Repos**: GitHub Token erforderlich
- **Large Repos**: "Quick" Analysis für ersten Test

### **Analysis Types**
- **Quick** (5 min): Für erste Einschätzung
- **Standard** (15 min): Für normale Bewertung  
- **Comprehensive** (30 min): Für vollständige Due Diligence

### **Cost Optimization**
- **Bedrock Kosten**: ~$0.03 per 1K tokens
- **Typical Analysis**: $0.50 - $2.00
- **Batch Processing**: Mehrere Repos gleichzeitig

## 🚀 **Production Deployment**

### **Environment Variables (Production)**
```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=prod_access_key
AWS_SECRET_ACCESS_KEY=prod_secret_key

# Security
DEBUG=false
LOG_LEVEL=WARNING
CORS_ORIGINS=https://yourdomain.com

# Analysis Limits
MAX_CONCURRENT_ANALYSES=5
TEMP_DIR_PREFIX=/tmp/ai_mvise_
```

### **Docker Support**
```dockerfile
# Dockerfile example
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📈 **Monitoring & Analytics**

- **Health Checks**: `/api/health`
- **Metrics**: Analysis completion rates
- **Costs**: Bedrock token usage
- **Performance**: Average analysis time

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Submit Pull Request

## 📄 **License**

MIT License - see LICENSE file for details.

---

## 🎉 **Ready to Go!**

Das System ist jetzt bereit für **echte AI-gestützte Repository-Analyse** mit **Amazon Bedrock Claude**! 

**Nächste Schritte:**
1. ✅ AWS Bedrock Zugriff aktivieren
2. ✅ Credentials konfigurieren  
3. ✅ System starten: `npm run dev`
4. 🚀 Ersten Repository analysieren!

**Für Support**: Logs prüfen und Troubleshooting-Sektion befolgen. 