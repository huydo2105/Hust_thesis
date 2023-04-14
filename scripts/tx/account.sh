#!/bin/bash

# forget addresses
octez-client forget address harry --force
octez-client forget address zayn --force

# import secret keys
octez-client import secret key harry unencrypted:${SECRET_KEY_HARRY}
octez-client import secret key zayn unencrypted:${SECRET_KEY_ZAYN}

# reveal keys
octez-client reveal key for harry
octez-client reveal key for zayn

# transfer funds
octez-client --wait none transfer 100 from harry to zayn --burn-cap 0.654