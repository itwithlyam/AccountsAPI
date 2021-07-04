# AccountsAPI
A template API for a basic accounts system.

## Methods
[x] GET
[x] POST
[ ] PUT
[x] PATCH
[x] DELETE

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
[x] Home access
[ ] GET access
[ ] POST access
[ ] PUT/PATCH access
[ ] DELETE access
[ ] ROOT access
### Level 2
[x] Home access
[x] GET access
[ ] POST access
[ ] PUT/PATCH access
[ ] DELETE access
[ ] ROOT access
### Level 3
[x] Home access
[x] GET access
[x] POST access
[x] PUT/PATCH access
[ ] DELETE access
[ ] ROOT access
### Level 4
[x] Home access
[x] GET access
[x] POST access
[x] PUT/PATCH access
[x] DELETE access
[x] ROOT access
