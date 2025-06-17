# Collateral Description Agent PoC
This is just a PoC, the final version could be different in architecture and technology.

## Quickstart

1. Copy the *.env.sample* file and rename it to *.env*
2. Fill the *.env* file with the empty [environment variables](#env-vars). Also can configure the others for your taste.
3. Navigate the shell to the root directory of this repo: `cd collateral-description-agent`

### Python
4. (Optional, but recommended) Create a [virtual environment](https://docs.python.org/3/library/venv.html) and activate it
5. Install required packages: `pip install -r requirements.txt`
6. Place the images of a single asset to the data folder
7. Start telemetry service with `python -m phoenix.server.main serve`
8. Start the app with `python app/app.py loadenv` (loadenv flag is for loading the environment variables)
9. You can check the telemetry and follow the calls on http://localhost:6006

### Docker
4. Create a docker image using the *Dockerfile* with `docker build --tag collateral-agent .`
5. Run the docker container passing the `.env` file and mapping the folder containing the images
```
docker run -p 6006:6006 --env-file .env \
    -v <folder-containing-images>:/data:ro \
    collateral-agent
```
6. Navigate to `https://localhost:6006` on your browser

## Env vars

| Variable name           | Description                                                                                                                                                                        |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OPENAI_API_KEY          | OpenAI API key                                                                            |


## Architecture
![architecture diagram of the application](documentation/architecture.png "Architecture")