#!/bin/bash

# append to myContract.tz
cat >> myContract.tz <<EOL
parameter string;
storage string;
code { UNPAIR ; PUSH string "," ; CONCAT ; SWAP ; CONCAT ; NIL operation ; PAIR }
EOL

octez-client originate contract myContract transferring 0 from harry runnin
g myContract.tz --init '"Hello"' --burn-cap 0.1

octez-client transfer 0 from harry to KT1E9MY9M4qNuxt7mscfaYmEKnVDvbKYtXTr --entrypoint "default" --arg "\"hello\"" --dry-run --burn-cap 1

