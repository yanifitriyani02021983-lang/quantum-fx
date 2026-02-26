📈 Quantum-FX: AI-Driven Web Trading System


Sistem trading forex berbasis web kelas institusional dengan integrasi MetaTrader 5, ditenagai oleh Multi-Model AI (LSTM+Attention, Transformer, RL) dan sistem Manajemen Risiko tingkat lanjut.


📂 Struktur Folder Project (GitHub-Ready)

quantum-fx/
│
├── frontend/                  # Web Dashboard (React.js / Next.js)
│   ├── src/components/        # Charting (TradingView Lightweight Charts), Control Panel
│   └── src/pages/             # Dashboard, Risk Metrics, AI Training Status
│
├── backend/                   # FastAPI Backend
│   ├── api/                   # REST / GraphQL Endpoints
│   ├── core/                  # Konfigurasi, Security (JWT)
│   ├── mt5_bridge/            # Koneksi ZeroMQ / Python ke MetaTrader 5 Terminal
│   └── websockets/            # Streaming harga realtime ke Frontend via Redis Pub/Sub
│
├── ai_engine/                 # Sistem AI & Machine Learning
│   ├── data_pipeline/         # Ekstraksi fitur (EMA, SMA, MACD, RSI, ATR, ADX, SMC)
│   ├── models/                # Arsitektur PyTorch (LSTM, Transformer, RL Agent)
│   ├── trainers/              # Script training & Retraining mingguan otomatis
│   └── ensemble/              # XGBoost + Deep Learning Aggregator
│
├── risk_management/           # Modul Manajemen Risiko & Simulasi
│   ├── monte_carlo.py         # 100k Scenario Simulator
│   ├── risk_of_ruin.py        # Kalkulator kebangkrutan
│   └── crisis_detector.py     # Anomaly Detection untuk News Impact (Black Swan)
│
├── docker/                    # Infrastruktur Docker
│   ├── docker-compose.yml
│   ├── postgres/              # Init scripts untuk TimescaleDB/Postgres
│   └── mysql/                 # Init scripts untuk MySQL
│
├── scripts/                   # Shell scripts untuk deploy & cron jobs (Weekly Retrain)
├── requirements.txt           # Python dependencies
└── README.md                  # Dokumentasi ini




🏗️ Arsitektur Sistem Lengkap
Data Ingestion (MT5 -> DB): Terminal MT5 mengirim tick data dan OHLCV ke sistem. Redis menampung data realtime, sementara PostgreSQL (idealnya dengan ekstensi TimescaleDB) menyimpan histori panjang.
Feature Engineering: Cron job mengkalkulasi indikator teknikal konvensional (EMA, MACD, dll) dan Smart Money Concept (Fair Value Gaps, Liquidity Sweeps).


AI Inference (Realtime): Data masuk ke model Ensemble (LSTM + XGBoost). Model memprediksi arah (Direction), sementara AI pendukung memprediksi Volatilitas (untuk set TP/SL dinamis).


Risk & Crisis Guard: Sebelum eksekusi, sinyal melewati Crisis Detector (Isolation Forest). Jika ada anomali tinggi (misal: rilis NFP/CPI), sistem beralih ke mode protektif atau halt trading. Sinyal juga divalidasi oleh perhitungan Risk of Ruin.


Execution: Sinyal valid dikirim kembali ke MT5 via Python MetaTrader5 library. Frontend React menerima status update via WebSockets.


Continuous Learning: Setiap akhir pekan (Sabtu/Minggu), pipeline Retraining aktif otomatis untuk fine-tuning bobot model dengan data seminggu terakhir agar AI tetap adaptif.


🗄️ Desain & Skema Database (SQL)
Sistem menggunakan arsitektur Polyglot Persistence untuk optimalisasi performa.

1. PostgreSQL (Time-Series Data & Market Data)
Digunakan untuk menyimpan data historis candlestick dan tick yang berat.

-- Table: ohlcv_data
CREATE TABLE ohlcv_data (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    timeframe VARCHAR(5) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    open NUMERIC(10, 5),
    high NUMERIC(10, 5),
    low NUMERIC(10, 5),
    close NUMERIC(10, 5),
    tick_volume BIGINT,
    spread INTEGER,
    UNIQUE(symbol, timeframe, timestamp)
);
CREATE INDEX idx_ohlcv_symbol_time ON ohlcv_data(symbol, timestamp DESC);

-- Table: smart_money_concepts (SMC & Liquidity)
CREATE TABLE market_structure (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10),
    timestamp TIMESTAMPTZ,
    type VARCHAR(20), -- 'BOS' (Break of Structure), 'CHoCH', 'Liquidity Sweep'
    price_level NUMERIC(10, 5),
    is_mitigated BOOLEAN DEFAULT FALSE
);


2. MySQL (Relational Data, Users, Trading Logs)

Digunakan untuk manajemen user web, konfigurasi risk, dan pencatatan trade untuk akuntansi.
-- Table: users
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'trader', 'viewer') DEFAULT 'trader',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: trade_history
CREATE TABLE trade_history (
    ticket_id BIGINT PRIMARY KEY,
    user_id INT,
    symbol VARCHAR(10),
    order_type VARCHAR(10), -- BUY / SELL
    volume DECIMAL(10, 2),
    open_price DECIMAL(10, 5),
    close_price DECIMAL(10, 5),
    sl DECIMAL(10, 5),
    tp DECIMAL(10, 5),
    profit DECIMAL(10, 2),
    ai_model_used VARCHAR(50), -- Model mana yang memberi sinyal
    open_time DATETIME,
    close_time DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Table: ai_performance_metrics
CREATE TABLE ai_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(50),
    week_start DATE,
    win_rate DECIMAL(5, 2),
    profit_factor DECIMAL(5, 2),
    max_drawdown DECIMAL(5, 2)
);


3. Redis (In-Memory Data Store)
Menyimpan Live Tick Data untuk kecepatan milidetik.
Redis Pub/Sub untuk menyiarkan sinyal AI langsung ke Web Dashboard dan modul eksekusi MT5.
Caching hasil inferensi AI sementara.
