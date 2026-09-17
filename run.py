"""
VerifyAI One-Click System Launcher
Starts both the FastAPI Backend (:8000) and the Streamlit Dashboard (:8501)
"""
import subprocess
import sys
import time
import os
import signal

def main():
    print("=" * 65)
    print("🛡️  VerifyAI - AI-Powered Identity Verification Platform")
    print("    AI Build Challenge Bengaluru | PS-003 Hackingly")
    print("=" * 65)
    print("\nStarting services...")

    # Ensure database and sample images are ready
    try:
        from app.database import init_db
        init_db()
        print("✅ Database initialized (data/verifyai.db)")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")

    # 1. Start FastAPI API Server
    print("🚀 Launching FastAPI Backend on http://localhost:8000 ...")
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    time.sleep(2)

    # 2. Start Streamlit Dashboard
    print("📊 Launching Streamlit Organizer Dashboard on http://localhost:8501 ...")
    dash_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "dashboard/app.py", "--server.port", "8501"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    print("\n" + "=" * 65)
    print("✨ ALL SERVICES ARE LIVE!")
    print("   👉 Organizer Dashboard: http://localhost:8501")
    print("   👉 API Documentation:   http://localhost:8000/docs")
    print("   👉 Health Check:        http://localhost:8000/api/v1/health")
    print("=" * 65)
    print("\nPress Ctrl+C to terminate all services.\n")

    def signal_handler(sig, frame):
        print("\nStopping services...")
        api_process.terminate()
        dash_process.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        api_process.terminate()
        dash_process.terminate()
        print("\nServices terminated.")

if __name__ == "__main__":
    main()
