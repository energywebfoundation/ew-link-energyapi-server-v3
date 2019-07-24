# ew-link-energyapi-server-v3
A server implementation of the Energy Measurement API: http://165.227.133.50:6969/

## Development

This is using Python 3.7 and pipenv.

### git
Clone this repository

### Build
```
cd ew-link-energyapi-server-v3
pipenv shell
pipenv sync
```

### Run

```
./resetdb.py
./server.py
```

The server is listening on: http://localhost:5000/
An UI is availbale at: http://localhost:5000/v3/ui

Call the API: `curl http://localhost:8080/v3/produced/0`

## OpenAPI Definition

The API definition is in the file swagger.yml which is managed at Swagger Hub.