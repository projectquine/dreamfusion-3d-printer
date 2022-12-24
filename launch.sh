# Replay YOUR_NGROK_TOKEN with your token from https://dashboard.ngrok.com/get-started/your-authtoken
ngrok config add-authtoken YOUR_NGROK_TOKEN

# Start ngrok in the background
ngrok http 8000 > /dev/null &

# Wait 2 seconds and then grab our ngrok tunnel url
sleep 2
export NGROK_URL=$(curl http://localhost:4040/api/tunnels | jq ".tunnels[0].public_url")
echo " "
echo "DF-API is running at: $NGROK_URL"
echo " "
# Start the dreamfusion API
uvicorn main:app --reload