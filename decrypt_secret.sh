#!/bin/sh

# Decrypt the file
#mkdir $HOME/secrets
# --batch to prevent interactive command
# --yes to assume "yes" for questions
gpg --quiet --batch --yes --decrypt --passphrase="$LARGE_SECRET_PASSPHRASE" \
--output FellowKey.ionapi  FellowKey.ionapi.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$LARGE_SECRET_PASSPHRASE" \
--output FellowConsulting_Cloud.ionapi  FellowConsulting_Cloud.ionapi.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$LARGE_SECRET_PASSPHRASE" \
--output credentials/credentials.ionapi  credentials/credentials.ionapi.gpg