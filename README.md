# Finance News Intelligence Agent

A cloud-ready finance digest system that fetches business news and FX rates, generates a daily digest report, and provides a Streamlit-based dashboard.

This project demonstrates a simple cloud architecture design + CI/CD pipeline + Infrastructure as Code (IaC) skeleton.

---

## Demo (Local)

After running, open:

- http://localhost:8501

The dashboard will display:
- Latest business news (Newsdata.io API)
- FX snapshot (open.er-api.com / exchangerate API)

---

## Features

- **Streamlit dashboard (Python frontend)**
- Fetch business news via **Newsdata.io API**
- Fetch FX rates via **open exchange rate API**
- **Worker service** to generate a daily digest HTML file (`digest.html`)
- Docker-ready structure (app + worker)
- GitHub Actions CI pipeline
- Cloud architecture design (AWS)
- Git Flow design for collaboration
- Infrastructure as Code (Terraform skeleton)

---

## Tech Stack

- Python 3.11
- Streamlit
- Requests
- Docker (optional)
- GitHub Actions (CI)
- Terraform (IaC skeleton)

---

## APIs Used

- **Newsdata.io** (Business News API)
- **FX API** (Exchange Rate API)

---

## Project Structure

```

finance-news-intelligence-agent/
├── app/                       # Streamlit frontend
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── worker/                    # Digest generator
│   ├── run_worker.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── infra/                     # Terraform IaC skeleton (AWS)
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── vpc.tf
│   ├── ecs.tf
│   ├── s3.tf
│   ├── rds.tf
│   └── iam.tf
│
├── docs/                      # Architecture diagrams
│   ├── cloud-architecture.png
│   ├── cicd-flow.png
│   └── git-flow.png
│
├── .github/workflows/         # CI pipeline
│   └── ci.yml
│
├── output/                    # Generated digest output
├── docker-compose.yml
├── .gitignore
└── README.md

````

---

## Setup

### 1) Create `.env`

Create a `.env` file in the project root:

```bash
NEWSDATA_API_KEY=YOUR_API_KEY_HERE
````

⚠️ Do NOT commit `.env` to GitHub.

---

## Run Locally

### Option A: Run Streamlit directly (Recommended)

```bash
cd app
pip install -r requirements.txt
streamlit run main.py
```

---

### Option B: Run with `.env` auto load

```bash
set -a
source .env
set +a

cd app
pip install -r requirements.txt
streamlit run main.py
```

---

## Run Worker (Generate Digest HTML)

The worker will generate a report file:

* `output/digest.html`

Run worker locally:

```bash
set -a
source .env
set +a

cd worker
pip install -r requirements.txt
python run_worker.py
```

After running, check:

```bash
ls output/
```

---

## Docker Compose (Optional)

If Docker is installed, you can run everything with one command:

```bash
docker compose up --build
```

Then open:

* [http://localhost:8501](http://localhost:8501)

---

## Output

The worker generates a daily digest report:

* `output/digest.html`

This file contains:

* FX snapshot section
* Top business news section

---

## CI/CD Pipeline (GitHub Actions)

This project includes a CI pipeline (`.github/workflows/ci.yml`) that automatically runs on:

* push to `main`
* pull request

CI tasks include:

* install dependencies
* verify build environment
* docker build (app + worker)

---

## Git Flow (Collaboration)

Recommended workflow:

* `feature/*` → Pull Request → `develop`
* `develop` → release merge → `main`
* `hotfix/*` → patch merge → `main`

See diagram:

* `docs/git-flow.png`

---

## Cloud Architecture Design (AWS)

This repository provides a cloud architecture design for deploying the system on AWS.

Core components:

* CloudFront + WAF + ALB
* ECS Fargate (Streamlit frontend)
* EventBridge Scheduler (trigger worker job)
* ECS Task (Worker)
* S3 (store digest reports)
* RDS (store metadata, optional)
* CloudWatch Logs

See diagram:

* `docs/cloud-architecture.png`

---

## Infrastructure as Code (Terraform)

Terraform skeleton is provided under `infra/` to demonstrate IaC.

Includes:

* VPC
* ECS cluster
* S3 bucket
* RDS instance skeleton
* IAM roles

⚠️ This is a skeleton template for academic demonstration and is not production-hardened.

---

## Notes

* `.env` is ignored by `.gitignore`
* For security, API keys should only be stored in `.env` or secret managers
* For real production deployment, API keys should be stored in AWS Secrets Manager

---

## Author

Cindy Wang
GitHub: [https://github.com/CindyWang1126](https://github.com/CindyWang1126)

