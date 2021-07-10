# AccountsAPI
A template API for a basic accounts system.

## Methods
- [x] GET
- [x] POST
- [ ] PUT
- [x] PATCH
- [x] DELETE

## Authorization
**Access tokens to be set in `administrators.json`**
### Schema
```json
"username": {
    "name": 1 (number),
    "level": Permission level (number),
    "check": Access token (string),
    "method": Hashing algotrithm (string)
}
```
### Level 1
- [x] Home access
- [ ] GET access
- [ ] POST access
- [ ] PUT/PATCH access
- [ ] DELETE access
- [ ] ROOT access
### Level 2
- [x] Home access
- [x] GET access
- [ ] POST access
- [ ] PUT/PATCH access
- [ ] DELETE access
- [ ] ROOT access
### Level 3
- [x] Home access
- [x] GET access
- [x] POST access
- [x] PUT/PATCH access
- [ ] DELETE access
- [ ] ROOT access
### Level 4
- [x] Home access
- [x] GET access
- [x] POST access
- [x] PUT/PATCH access
- [x] DELETE access
- [x] ROOT access

## Running
The API is built on Python, which means that it is easy to run.

**Dependencies:**

`mysql.connector`: ```pip install mysql.connector```

`flask`: ```pip install flask```

`waitress`: ```pip install waitress```

### Deployment
1. Create a new virtual envrionment using `python -m venv venv`
2. Move the files into the virtual environment
3. Activate the virtual environment via `bash bin/activate` on MacOS and Linux or `scripts/activate` on Windows
4. Install `waitress` as shown above and run `waitress-serve --port 80 "v2:app"`. On MacOS and Linux, run this with `sudo` permissions.
5. Head to 127.0.0.1 (localhost) and onto your desired enpoint.

### Test suite
1. Install Node.JS and npm: https://nodejs.org
2. Install `node-fetch` using `npm install node-fetch`
4. Edit the test suite to your desired enpoint and URL
5. Run `node testing.js` in a different terminal to the one with your API. Make sure you keep the API running!
