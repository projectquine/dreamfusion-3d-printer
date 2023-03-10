## Usage:

To start a run of the training we do a POST to the /model endpoint with the "text" for the prompt we want to try:
```
curl -X 'POST' \
  'http://localhost:8000/model/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "plastic toy frog wearing a top hat"
}'
```
This will return us a uri with a `UUID` that we will use for later requests, so keep that handy. Note you can also add `"iterations": 30000` to the request body and increase or decrease the number of iterations. The default is 10000.

To get the object (.obj) file we do a GET:
```
curl -X 'GET' 'http://localhost:8000/model/<YOUR_UUID>/obj' -H 'accept: application/json' --output result.obj
```

To get the .mtl file we do a GET:
```
curl -X 'GET' 'http://localhost:8000/model/<YOUR_UUID>/mtl' -H 'accept: application/json' --output result.mtl
```
**Note: If the file is not found, the API returns a 404, but curl will just save that response into the output file anyway :/ **

To fetch a results video file, use curl rather than the /docs endpoint:
```
curl -X 'GET' 'http://localhost:8000/model/<YOUR_UUID>/result' -H 'accept: application/json' --output result.mp4
```

We can also periodically check the validation PNGs to see how the training is going, to do this we query the /validation endpoint with:
```
curl -X 'GET' 'http://localhost:8000/model/<YOUR_UUID>/validation' -H 'accept: application/json' --output latest-validation.png
```
Note: The validation files are only updated every 3 or 4 minutes, so no point hammering the endpoint :D

## Setup Server:

1. Create an account on lambdalabs.com and create an A100 instance. 
2. ssh into the instance and run:
```
git clone https://github.com/ashawkey/stable-dreamfusion.git
cd stable-dreamfusion
``` 
3. Install apt dependencies:
```
sudo apt-get update && sudo apt-get install pybind11-dev python3-pybind11
```
4. Install python dependencies:
```
pip install -r requirements.txt
# (optional) install nvdiffrast for exporting textured mesh (if use --save_mesh)
pip install git+https://github.com/NVlabs/nvdiffrast/
```
5. To test the setup run a quick train example. Note that the first run will take a while (5-10 minutes) to start up as loads all the extensions, etc.
```
python main.py --text "a hamburger" --workspace trial -O --iters 100
```
6. After the run finished, generate the results and mesh:
```
python main.py --workspace trial -O --test --save_mesh
```
6. `git clone https://github.com/shaunmulligan/df-api.git` into the root where you cloned stable-dreamfusion
7. To start the server run: `./launch.sh
8. To open a port to the internet you can use `ngrok` to create a tunnel to the local server:
```
ngrok http 8000
```
then the output will give you a public url something like:
```                                                                                         
Forwarding                    https://ca1f-132-145-142-210.ngrok.io -> http://localhost:8000                                                               
```
