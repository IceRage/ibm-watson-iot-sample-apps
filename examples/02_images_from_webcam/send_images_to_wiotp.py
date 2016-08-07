#!/usr/bin/env python

import argparse
import pickle
import sys

from cv2 import *

import ibmiotf.device



# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

OPENCV_WIN_NAME = "WebCamera";


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def initCameraClient():
    """
        Initialize the web camera client.

        Args:
            None.

        Returns:
            An instance of cv2.VideoCapture representing the camera client.

        Raises:
            None.
    """
    try:
        cameraClient = VideoCapture(0);

        return cameraClient;
    except Exception as exception:
        print("Could not initialize the web camera: %s" % str(exception));

        sys.exit(1);

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

def getDeviceEventPayload(cameraClient):
    """
        Get a dictionary instance representing the device event payload.

        Args:
           cameraClient: An instance of cv2.VideoCapture used to communicate with the local webcam. 

        Returns:
            A dictionary instance representing the device event payload.

        Raises:
            None.
    """
    # Capture an image using the webcam
    okMsg, image = cameraClient.read();

    # If no error occurred
    if okMsg:
        # Show the image that will be sent
        imshow(OPENCV_WIN_NAME, image);

        # Reduce the image size by a factor of 10 to reduce the size of the payload
        imageScaled = resize(image, None, fx = 0.1, fy = 0.1, interpolation = INTER_CUBIC);

        # Serialize image using pickle
        imgPayload = pickle.dumps(imageScaled);
    else:
        imgPayload = "Could not capture image from webcam.";

    # Prepare device event payload
    data = {"img" : imgPayload};

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

# Create camera client
cameraClient = initCameraClient();

# Create device client
deviceClient = initDeviceClient(options.organizationId, options.deviceType, options.deviceId, 
                                options.authMethod, options.authToken);

# Initialize the window in which the captured images are displayed
namedWindow(OPENCV_WIN_NAME, WND_PROP_FULLSCREEN);

# Connect device client
deviceClient.connect();

# Send data whenever the user presses a key different from 'q'
keyPressed = 0;

while chr(keyPressed & 255) != 'q':
    # Prepare data to be sent
    data = getDeviceEventPayload(cameraClient);

    # Send data
    deviceClient.publishEvent(options.deviceEventName, options.deviceEventFormat, data);

    # Wait for a new key to be pressed up to one second
    keyPressed = waitKey(1000);

# Destroy the window used to display images
destroyWindow(OPENCV_WIN_NAME);

# Disconnect device client
deviceClient.disconnect();
