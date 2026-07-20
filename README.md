# HHAR Activity Recognition Web App

An end-to-end Human Activity Recognition project built on the UCI Heterogeneity Activity Recognition (HHAR) dataset. The repository includes:

- A reusable machine learning pipeline for downloading, preprocessing, training, and evaluating the model
- A FastAPI backend for inference and project metadata
- A React + Vite + Tailwind frontend for interactive predictions
- Deployment configuration for Render and Vercel

## Project Structure

```text
.
|-- backend/
|-- data/
|-- docs/
|-- frontend/
|-- ml/
|-- .env.example
|-- Dockerfile
|-- render.yaml
|-- requirements.txt
|-- vercel.json
```

## Dataset

This project targets the UCI Heterogeneity Activity Recognition dataset:

- Dataset page: https://archive.ics.uci.edu/dataset/344/heterogeneity+activity+recognition
- License: CC BY 4.0

The training pipeline downloads the activity-recognition ZIP directly from UCI and uses the smartphone accelerometer and gyroscope streams.

## Backend Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn backend.app.main:app --reload
```

API will start at `http://localhost:8000` and docs will be available at `http://localhost:8000/docs`.

## Machine Learning Workflow

Train the model from the repository root:

```bash
python -m ml.src.train --sample-fraction 0.05
```

Optional flags:

- `--sample-fraction`: Fraction of rows sampled from each sensor stream before merging
- `--random-state`: Reproducible training seed
- `--force-download`: Re-download dataset archive even if already cached

Artifacts generated:

- `ml/artifacts/hhar_random_forest.joblib`
- `ml/artifacts/hhar_scaler.joblib`
- `ml/artifacts/hhar_label_encoder.joblib`
- `ml/artifacts/metrics.json`
- `ml/reports/confusion_matrix.png`
- `ml/reports/classification_report.csv`

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Create `frontend/.env` if needed:

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

The Vite app runs at `http://localhost:5173`.

## Deployment

### Render

1. Create a new Web Service from this repository.
2. Use the root `Dockerfile`, or use `render.yaml` for blueprint deployment.
3. Set environment variables from `.env.example`.
4. Ensure model artifacts exist in `ml/artifacts` by training before deployment or running the training job in CI/CD.

### Vercel

1. Import the repository into Vercel.
2. Set project root to `frontend`.
3. Add `VITE_API_BASE_URL` pointing at the deployed Render backend.
4. Deploy using the included `vercel.json`.

## Validation Checklist

- Backend imports validated with `python -m compileall`
- API routes organized under `/api/v1`
- Frontend service layer points to the backend base URL
- Deployment files and environment templates included

## Screenshots

Placeholder assets are available in [docs/screenshots](/C:/Users/Asus/Documents/New%20project/docs/screenshots).

## Manual Steps Before Production Deployment

1. Run the training command to generate fresh model artifacts locally or in CI.
2. Install Node.js 20+ to build the frontend locally.
3. Run `npm install && npm run build` inside `frontend`.
4. Deploy backend to Render and frontend to Vercel with the correct environment variables.

