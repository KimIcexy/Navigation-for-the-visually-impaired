// This is just a testing page
import * as React from 'react';
import { useState, useEffect, useRef, useCallback } from 'react';
import { Text, View, Pressable, TextInput, StyleSheet, Alert } from 'react-native';
import { Camera } from 'expo-camera';
import * as Linking from 'expo-linking';

import { CameraFaceSettings } from '../Constant/Camera.jsx';

const FaceDetection = ({ navigation }) => {
    const [detectedFaces, setDetectedFaces] = useState([]);

    const [cameraStatus, requestCameraPermission] = Camera.useCameraPermissions();

    const handleCameraPermission = useCallback(async () => {
        if (!cameraStatus) {
            return ;
        }
        if ((cameraStatus.status === 'undetermined') || ((cameraStatus.status === 'denied') && cameraStatus.canAskAgain)) {
            const permission = await requestCameraPermission();
            if (permission.status === 'granted') {
                return ;
            }
            else {
                
            }
        }
        else if (cameraStatus.status === 'denied') {
            Alert.alert(
                'Quyền truy cập camera bị từ chối',
                'Vui lòng cấp quyền truy cập camera để sử dụng tính năng này',
                [
                    {
                        text: 'OK',
                        onPress: () => {
                            Linking.openSettings();
                            navigation.navigate('Home');
                        }
                    },
                    {
                        text: 'Cancel',
                        onPress: () => {
                            navigation.navigate('Home');
                        }
                    }
                ]
            )
        }
        else {
            return ;
        }
    }, [cameraStatus]);

    handleCameraPermission();

    const onFacesDetected = ({ faces }) => {
        if (faces.length > 0) {
            setDetectedFaces(faces);
        }
        else {
            setDetectedFaces([]);
        }
    }

    const faceBoundingBox = () => {
        if (detectedFaces.length === 0) return ;
        return detectedFaces.map((face, index) => {
            if (face.bounds === undefined) return ;
            const {origin, size} = face.bounds;
            const {x, y} = origin;
            const {width, height} = size;
            return (
                <View
                    key={index}
                    style={{
                        position: 'absolute',
                        left: x,
                        top: y,
                        width: width,
                        height: height,
                        borderWidth: 2,
                        borderColor: '#00FF00',
                        borderRadius: 5,
                    }}
                />
            )
        })
    }


    return (
        <View style={{display: 'flex', flex: 1}}>
            <Camera
                style={{display: 'flex', flex: 1}}
                type={Camera.Constants.Type.front}
                faceDetectorSettings={CameraFaceSettings}
                onFacesDetected={onFacesDetected}
            />
            {faceBoundingBox()}
        </View>
    )
}

export default FaceDetection;