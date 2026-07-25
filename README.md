# xLSTM Colorization Application

An industrial-grade, full-stack application for B&W Image Colorization using a custom pure-PyTorch mLSTM implementation.

## 📂 Project Structure

- `backend/`: FastAPI application containing the PyTorch model and endpoints.
- `frontend/`: React + Vite application featuring a brutalist, engineering workstation UI.

## 🛠️ Setup Instructions

### 1. Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your trained Kaggle model:
   - Place your `xlstm_colorizer_epoch_10.pth` (or best epoch) into `backend/checkpoints/`
   - Rename it to `best_model.pth`.
4. Run the API:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

### 2. Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies (Requires Node.js):
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## 📝 Design Note

A fully interactive prototype of the requested Frontend UI has been generated as a standalone `dashboard-preview.html` file in the root directory. You can open it in any web browser without needing to run `npm install`.
