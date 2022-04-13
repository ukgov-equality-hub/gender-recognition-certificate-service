
# Get parameters
PAAS_SPACE_NAME=$1
PAAS_DATABASE_NAME=$2
PAAS_DATABASE_KEY_NAME=$3
LOCAL_PORT=$4


# Login
./LoginToGovPaaS.sh


# Target future commands at the right space
cf target -s "${PAAS_SPACE_NAME}"



# Fetch the keys that you might want to use to connect to the database or cache
echo ""
echo "======================================="
echo "HERE ARE THE KEYS YOU MIGHT WANT TO USE"
echo "======================================="
echo ""

echo "Host: 127.0.0.1"
echo "Port: ${LOCAL_PORT}"
echo "Username & Password: see below"
echo ""

cf service-key "${PAAS_DATABASE_NAME}" "${PAAS_DATABASE_KEY_NAME}"



# Connect to PaaS via Conduit
echo ""
echo "==========================="
echo "IGNORE KEYS PAST THIS POINT"
echo "==========================="
echo ""

# - Setup variables
DEVELOPER_MACHINE_NAME=$(hostname)
CONDUIT_APP_NAME="conduit-grc-${PAAS_SPACE_NAME}-db-${DEVELOPER_MACHINE_NAME}"

# - Delete any old conduit apps - sometimes they don't get cleared up correctly
cf delete "${CONDUIT_APP_NAME}" -f

# - Connect
cf conduit "${PAAS_DATABASE_NAME}" --local-port $LOCAL_PORT --space "${PAAS_SPACE_NAME}" --app-name "${CONDUIT_APP_NAME}"



# Wait for user input - just to make sure the window doesn't close without them noticing
echo ""
echo ""
read  -n 1 -p "Press Enter to finish:" unused
