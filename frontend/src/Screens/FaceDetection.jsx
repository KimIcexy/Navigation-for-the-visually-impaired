// This is just a testing page
import * as React from 'react';
import { useState, useEffect, useRef } from 'react';
import { Text, View, Pressable, TextInput, StyleSheet, Alert } from 'react-native';
import { Camera } from 'expo-camera';

import { CameraFaceSettings } from '../Constant/Camera.jsx';

const FaceDetection = () => {
    const [detectedFaces, setDetectedFaces] = useState([]);

    useEffect(() => {
        const getPermission = async () => {
            const { status } = await Camera.requestCameraPermissionsAsync();
            if (status !== 'granted') {
                Alert.alert('Quyền truy cập camera bị từ chối', 'Vui lòng cấp quyền truy cập camera để sử dụng tính năng đăng nhập bằng mặt người.');
                setIsFaceMethod(false); // Turn off face login
                return ;
            }
        }
        getPermission();
    }, []);

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