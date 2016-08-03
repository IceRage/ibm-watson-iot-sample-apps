#!/usr/bin/env python

import argparse
import pickle
import sys
import time

import ibmiotf.device

from cv2 import *


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

DEVICE_SND_EVT_NAME = "webcam";
DEVICE_SND_MSG_FMT  = "json";

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

        print("Connecting to device using options: %s" % str(deviceOptions));

        deviceClient = ibmiotf.device.Client(deviceOptions);

        return deviceClient;
    except Exception as exception:
        print("Caught exception connecting device: %s" % str(exception));

        sys.exit(2);

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

    parser.add_argument("-o", "--organization-id", action="store", required=True, dest="organization_id");
    parser.add_argument("-t", "--device-type", action="store", required=True, dest="device_type");
    parser.add_argument("-i", "--device-id", action="store", required=True, dest="device_id");
    parser.add_argument("-m", "--auth-method", action="store", required=True, dest="auth_method");
    parser.add_argument("-a", "--auth-token", action="store", required=True, dest="auth_token");

    # Parse command line options
    options = parser.parse_args();

    return options;


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

# Parse command line options
options = parseCommandLineOptions();

# Initialize web camera and device clients
cameraClient = initCameraClient();
deviceClient = initDeviceClient(options.organization_id, options.device_type, options.device_id, 
                                options.auth_method, options.auth_token);

# Initialize the window in which the captured images are displayed
namedWindow(OPENCV_WIN_NAME, WND_PROP_FULLSCREEN);

# Connect device client
deviceClient.connect();

# Send 1 image every second until the key "q" is pressed
keyPressed = 0;

while chr(keyPressed & 255) != 'q':
    # Prepare data to be sent
    data = getDeviceEventPayload(cameraClient);

    # Send the image
    deviceClient.publishEvent(DEVICE_SND_EVT_NAME, DEVICE_SND_MSG_FMT, data, qos = 1);

    # Wait for 1 second or until a key is pressed
    keyPressed = waitKey(1000);

# Destroy the window used to display images
destroyWindow(OPENCV_WIN_NAME);

# Disconnect device client
deviceClient.disconnect();
