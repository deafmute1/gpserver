Podcast sync server implementation that is (mostly) compatible with [gpodder.net API v2](https://gpoddernet.readthedocs.io/en/latest/api/index.html). 

# Deploying 
- Docker container TODO
- Make sure /api/admin is not hidden behind reverse proxy - no auth protection.

# Running Locally/Developing
1. Clone, setup venv and install poetry.
2. `poetry install` 
3. `poetry run gpserver`

const.py defualts should work for a dev environment.

Docs are available at `127.0.0.1:8000/{docs,redocs}`

# Known Good Clients
- N/A

# Implemented API Paths 
## Implemented from GPodder v2 - see gpodder or swagger docs for more info
- /api/2/subscriptions
- /api/2/auth

## Non-Gpodder Endpoints
- /api/admin

# Roadmap
## v1 Roadmap
- Docker
- Episode actions sync /api/2/episodes
- /subscriptions sync points
- /api/admin/modify
- More admin control

## Future 
- settings api
- favourites api
- devices api - maybe?
- web ui for account creation/management, maybe even playback and discovery.

## Do not implement?
- podcast list api
- directory api
- suggestions api