
########################
# Start of configuration

# Space Name
PAAS_SPACE_NAME="staging"

# Database Name
PAAS_DATABASE_NAME="postgres-13-staging"

# Database Key Name
PAAS_DATABASE_KEY_NAME="postgres-13-staging-developerkey"

# The local port to use
LOCAL_PORT=7200



#################
# Start of script

# Run the Conduit.sh command with the above environment variables set
./Conduit.sh $PAAS_SPACE_NAME $PAAS_DATABASE_NAME $PAAS_DATABASE_KEY_NAME $LOCAL_PORT
