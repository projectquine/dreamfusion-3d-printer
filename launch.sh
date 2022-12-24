# Replay YOUR_NGROK_TOKEN with your token from https://dashboard.ngrok.com/get-started/your-authtoken
ngrok config add-authtoken YOUR_NGROK_TOKEN

# Start ngrok in the background
ngrok http 80 &

# Start the dreamfusion API
uvicorn main:app --reload
