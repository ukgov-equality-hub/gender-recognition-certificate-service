
########################
# Start of configuration

# Space Name
PAAS_SPACE_NAME="sandbox"

# Database Name
PAAS_DATABASE_NAME="postgres-13-dev"

# Database Key Name
PAAS_DATABASE_KEY_NAME="postgres-13-dev-developerkey"

# The local port to use
LOCAL_PORT=7100



#################
# Start of script

# Run the Conduit.sh command with the above environment variables set
./Conduit.sh $PAAS_SPACE_NAME $PAAS_DATABASE_NAME $PAAS_DATABASE_KEY_NAME $LOCAL_PORT
