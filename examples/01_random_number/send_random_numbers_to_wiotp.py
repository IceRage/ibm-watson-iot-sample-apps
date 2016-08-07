#!/usr/bin/env python

import argparse
import random
import sys

import ibmiotf.device


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def initDeviceClient(organizationId, deviceTypeId, deviceId, authMethod, authToken):
    """
        Initialize the device client.

        Args:
            organizationId: A string instance representing the organization id.
            deviceTypeId:   A string instance representing the device type id.
            deviceId:       A string instance representing the device id.
            authMethod:     A string instance representing the authentication method.
            authToken:      A string instance representing the authentication token.

        Returns:
            An instance of ibmiotf.device representing the device client.

        Raises:
            None.
    """
    # Initialize the device client.
    try:
        deviceOptions = {
            "org"           : organizationId, 
            "type"          : deviceTypeId, 
            "id"            : deviceId, 
            "auth-method"   : authMethod, 
            "auth-token"    : authToken
        };

        print("Creating device client using options: %s" % str(deviceOptions));

        deviceClient = ibmiotf.device.Client(deviceOptions);

        return deviceClient;
    except Exception as exception:
        print("Failed to create device client: %s" % str(exception));

        sys.exit(1);

def getDeviceEventPayload():
    """
        Get a dictionary instance representing the device event payload.

        Args:
            None.

        Returns:
            A dictionary instance representing the device event payload.

        Raises:
            None.
    """
    randomNumber = random.randint(0, 1000000);
    data         = {"number" : randomNumber};

    sys.stdout.write("Payload to be sent: %d" % randomNumber);

    return data;

def parseCommandLineOptions():
    """
        Parse the given command line options.

        Args:
            None.

        Returns:
            options: A argparse.Namespace instance representing the parsed command line options.
            
        Raises:
            arparse.error if one of the required command line options is missing.
    """
    parser = argparse.ArgumentParser();

    parser.add_argument("-o", "--organization-id", action="store", required=True, dest="organizationId");
    parser.add_argument("-t", "--device-type", action="store", required=True, dest="deviceType");
    parser.add_argument("-i", "--device-id", action="store", required=True, dest="deviceId");
    parser.add_argument("-m", "--auth-method", action="store", required=True, dest="authMethod");
    parser.add_argument("-a", "--auth-token", action="store", required=True, dest="authToken");
    parser.add_argument("-e", "--device-event-name", action="store", required=True, dest="deviceEventName");
    parser.add_argument("-f", "--device-event-format", action="store", required=True, dest="deviceEventFormat");

    # Parse command line options
    options = parser.parse_args();

    return options;


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

# Parse command line options
options = parseCommandLineOptions();

# Create device client
deviceClient = initDeviceClient(options.organizationId, options.deviceType, options.deviceId, 
                                options.authMethod, options.authToken);

# Connect device client
deviceClient.connect();

# Send data whenever the user presses a key different from "q"
while sys.stdin.readline() != "q\n":
    # Prepare data to be sent
    data = getDeviceEventPayload();

    # Send data
    deviceClient.publishEvent(options.deviceEventName, options.deviceEventFormat, data);

# Disconnect device client
deviceClient.disconnect();
