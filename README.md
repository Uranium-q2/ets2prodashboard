# ETS2 Super Dashboard 🚚💨

A high-fidelity, super-charged digital dashboard for **Euro Truck Simulator 2 (ETS2)**, viewable in any browser (desktop, tablet via Spacedesk, second monitor...). Built with a Flask backend and a slick SVG/CSS frontend — no image assets or extra dependencies needed. Runs natively or in Docker.

![Dashboard Preview](https://img.shields.io/badge/ETS2-Telemetry-blue) ![Flask](https://img.shields.io/badge/Flask-Python-green) ![Docker](https://img.shields.io/badge/Docker-ready-blue)

---

## ✨ Features

- **SVG Gauge Cluster**: Speedometer (0-140 km/h) and Tachometer (0-3000 RPM with redline) drawn live in the browser — crisp at any resolution, zero PNG assets.
- **On-Board Computer**: Gear display, cruise control, fuel range estimate, and total odometer.
- **Warning Light Strip**: Parking brake, engine, electrics, low/high beam, hazards, wipers — lights up exactly like the real truck.
- **Active Job Panel**: Cargo, destination, remaining distance and income, shown automatically when you're on a job.
- **Live Telemetry Sync**: Real-time polling via Funbit's ETS2 Telemetry Web Server with smooth needle animations (10 updates/sec).
- **Blinker Indicators**: Synchronized left/right turn signals.
- **Runs anywhere**: plain Python, or a single `docker compose up` — no PIL/Pillow or font files required.

---

## 🛠️ Prerequisites

1. **Euro Truck Simulator 2** installed on your PC.
2. **Funbit ETS2 Telemetry Web Server** running locally (default port `25555`).
3. Either **Docker Desktop** *or* **Python 3.x** to run the dashboard.
4. (Optional) **Spacedesk** or any web-based second screen tool to show it on a tablet.

---

## 🐳 Run with Docker (recommended)

```bash
docker compose up --build
```

Then open `http://localhost:5050` in any browser on the same PC (or on your tablet, using the PC's LAN IP: `http://<pc-ip>:5050`).

The container talks to the ETS2 telemetry server on your **host** machine via `host.docker.internal`, which is wired up automatically in `docker-compose.yml`. If your telemetry server runs on a different port, override it:

```bash
ETS2_API_URL=http://host.docker.internal:25555/api/ets2/telemetry docker compose up --build
```

---

## 🐍 Run with Python (no Docker)

```bash
pip install -r requirements.txt
python main.py
```

Open `http://localhost:5000`.

---

## 📦 Project Structure

```text
ets2-dashboard/
│
├── main.py                 # Flask backend server (polls ETS2 telemetry)
├── requirements.txt        # Python dependencies (Flask only)
├── Dockerfile              # Container image definition
├── docker-compose.yml      # One-command local deployment
└── templates/
    └── index.html          # Dashboard UI, SVG gauges & polling logic
```

---

## ⚙️ Configuration

| Env var         | Default                                                   | Description                          |
|-----------------|-------------------------------------------------------------|---------------------------------------|
| `ETS2_API_URL`  | `http://host.docker.internal:25555/api/ets2/telemetry`     | URL of the Funbit telemetry endpoint |

---

## 📄 License

MIT — see [LICENSE](LICENSE).
