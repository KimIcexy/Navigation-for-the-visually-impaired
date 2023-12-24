// This is just a testing page
import * as React from 'react';
import { useState } from 'react';
import { View } from 'react-native';
import { Camera } from 'expo-camera';

import { CameraFaceSettings } from '../Constant/Camera.jsx';
import { getCameraPermission } from '../Utils/camera.js';
import { BoundingBoxStyle } from '../Constant/Style.jsx';

const FaceDetection = ({ navigation }) => {
    const [detectedFaces, setDetectedFaces] = useState([]);

    getCameraPermission(navigation);

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
                    style={BoundingBoxStyle(x, y, width, height)}
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