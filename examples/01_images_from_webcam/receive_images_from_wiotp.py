#!/usr/bin/env python

import argparse
import json
import pickle
import sys
import time

import ibmiotf.application

from cv2 import *


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

APPLICATION_ID  = "MySampleWebCamApp";
DEVICE_EVT_NAME = "webcam";
OPENCV_WIN_NAME = "WebCamera";


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

        print("Connecting to application using options: %s" % str(appOptions));

        appClient = ibmiotf.application.Client(appOptions);

        return appClient;
    except Exception as exception:
        print("Caught exception connecting application: %s" % str(exception));

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

    # Unpickle the received event data
    image = pickle.loads(deviceEvent.data["img"]);
    
    # Display image
    imshow(OPENCV_WIN_NAME, image);

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

    parser.add_argument("-o", "--organization-id", action="store", required=True, dest="organization_id");
    parser.add_argument("-t", "--device-type", action="store", required=True, dest="device_type");
    parser.add_argument("-i", "--device-id", action="store", required=True, dest="device_id");
    parser.add_argument("-m", "--auth-method", action="store", required=True, dest="auth_method");
    parser.add_argument("-k", "--auth-key", action="store", required=True, dest="auth_key");
    parser.add_argument("-a", "--auth-token", action="store", required=True, dest="auth_token");

    # Parse command line options
    options = parser.parse_args();

    return options;


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

# Parse the command line options
options = parseCommandLineOptions();

# Initialize application client
appClient = initAppClient(options.organization_id, APPLICATION_ID, options.auth_method, 
                          options.auth_key, options.auth_token);

# Initialize the window in which the received images are displayed
namedWindow(OPENCV_WIN_NAME, WND_PROP_FULLSCREEN);

# Connect application client
appClient.connect();

# Subscribe to device events for the webcam device
appClient.subscribeToDeviceEvents(options.device_type, options.device_id, DEVICE_EVT_NAME);

# Set the callback for device events
appClient.deviceEventCallback = receivedDeviceEventCallback;

# While the key "q" was not pressed wait for new device events
keyPressed = 0;

while chr(keyPressed & 255) != 'q':
    keyPressed = waitKey(1000);

# Destroy the window used to display images
destroyWindow(OPENCV_WIN_NAME);

# Disconnect device client
appClient.disconnect();
