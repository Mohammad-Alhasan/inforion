#!/bin/sh

# Decrypt the file
#mkdir $HOME/secrets
# --batch to prevent interactive command
# --yes to assume "yes" for questions
gpg --quiet --batch --yes --decrypt --passphrase="$LARGE_SECRET_PASSPHRASE" \
--output $HOME/FellowKey.ionapi  $HOME/FellowKey.ionapi.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$LARGE_SECRET_PASSPHRASE" \
--output $HOME/FellowConsulting_Cloud.ionapi  $HOME/FellowConsulting_Cloud.ionapi.gpg

gpg --quiet --batch --yes --decrypt --passphrase="$LARGE_SECRET_PASSPHRASE" \
--output $HOME/credentials/credentials.ionapi  $HOME/credentials/credentials.ionapi.gpg