#!/usr/bin/env python

import argparse
import sys

import ibmiotf.application


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def initAppClient(organizationId, applicationId, authMethod, authKey, authToken):
    """
        Initialize the application client.

        Args:
            organizationId: A string instance representing the organization id.
            applicationId:  A string instance representing the application id.
            authMethod:     A string instance representing the authentication method.
            authKey:        A string instance representing the authentication key.
            authToken:      A string instance representing the authentication token.

        Returns:
            An instance of ibmiotf.application.Client representing the application client.

        Raises:
            None.
    """
    # Initialize the application client.
    try:
        appOptions = {
            "org"           : organizationId, 
            "id"            : applicationId, 
            "auth-method"   : authMethod, 
            "auth-key"      : authKey, 
            "auth-token"    : authToken
        };

        print("Creating application client using options: %s" % str(appOptions));

        appClient = ibmiotf.application.Client(appOptions);

        return appClient;
    except Exception as exception:
        print("Failed to create application client: %s" % str(exception));

        sys.exit(1);

def receivedDeviceEventCallback(deviceEvent):
    """
        Callback executed when a device event is received.

        Args:
            deviceEvent: The device event.

        Returns:
            None.

        Raises:
            None.
    """
    print("Received device event %s at %s for %s." % (deviceEvent.event, deviceEvent.timestamp.isoformat(), deviceEvent.device));

    data = deviceEvent.data;

    print("Received number: %d" % data["number"]);

def parseCommandLineOptions():
    """
        Parse the given command line options.

        Args:
            None.

        Returns:
            options: A argparse.Namespace instance containing the parsed command line options.
            
        Raises:
            argparse.error if one of the required command line options is missing.
    """
    parser = argparse.ArgumentParser();

    parser.add_argument("-o", "--organization-id", action="store", required=True, dest="organizationId");
    parser.add_argument("-p", "--application-id", action="store", required=True, dest="applicationId");
    parser.add_argument("-m", "--auth-method", action="store", required=True, dest="authMethod");
    parser.add_argument("-k", "--auth-key", action="store", required=True, dest="authKey");
    parser.add_argument("-a", "--auth-token", action="store", required=True, dest="authToken");
    parser.add_argument("-t", "--device-type", action="store", required=True, dest="deviceType");
    parser.add_argument("-i", "--device-id", action="store", required=True, dest="deviceId");
    parser.add_argument("-e", "--device-event-name", action="store", required=True, dest="deviceEventName");
    parser.add_argument("-f", "--device-event-format", action="store", required=True, dest="deviceEventFormat");

    # Parse command line options
    options = parser.parse_args();

    return options;


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

# Parse the command line options
options = parseCommandLineOptions();

# Create application client
appClient = initAppClient(options.organizationId, options.applicationId, options.authMethod, 
                          options.authKey, options.authToken);

# Connect application client
appClient.connect();

# Subscribe to device events
appClient.subscribeToDeviceEvents(options.deviceType, options.deviceId, options.deviceEventName, 
                                  options.deviceEventFormat);

# Set the callback for device events
appClient.deviceEventCallback = receivedDeviceEventCallback;

# While a key was not pressed wait for new device events
sys.stdin.readline();

# Disconnect device client
appClient.disconnect();
