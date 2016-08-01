#!/usr/bin/env python

import json
import pickle
import sys
import time

import ibmiotf.application

from cv2 import *


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

# TODO: Please update the values of these constans to match the details of your
#       own application.
ORGANIZATION_ID = "8aaaa8";
APPLICATION_ID  = "sampleWebcamApp";
AUTH_METHOD     = "apikey";
AUTH_KEY        = "a-8aaaa8-aaaaaaaaaa";
AUTH_TOKEN      = "aaaaaaaaaaaaaaaaaa";

DEVICE_TYPE     = "WebCamera";
DEVICE_ID       = "WebCameraMicrosoftHD";
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


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

# Initialize application client
appClient = initAppClient(ORGANIZATION_ID, APPLICATION_ID, AUTH_METHOD, AUTH_KEY, AUTH_TOKEN);

# Initialize the window in which the received images are displayed
namedWindow(OPENCV_WIN_NAME, WND_PROP_FULLSCREEN);

# Connect application client
appClient.connect();

# Subscribe to device events for the webcam device
appClient.subscribeToDeviceEvents(DEVICE_TYPE, DEVICE_ID, DEVICE_EVT_NAME);

# Set the callback for device events
appClient.deviceEventCallback = receivedDeviceEventCallback

# While the key "q" was not pressed wait for new device events
keyPressed = 0;

while chr(keyPressed & 255) != 'q':
    keyPressed = waitKey(1000);

# Destroy the window used to display images
destroyWindow(OPENCV_WIN_NAME);

# Disconnect device client
appClient.disconnect();
