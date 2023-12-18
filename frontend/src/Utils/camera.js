import { manipulateAsync } from 'expo-image-manipulator';
import { Camera } from 'expo-camera';
import { useCallback } from 'react';
import { Alert, Linking } from 'react-native';



// Desc: Camera utility functions, get an image from the camera and return it as base64
export const getImage = async (cameraRef) => {
    if (cameraRef) {
        const options = { base64: true };
        const imageFile = await cameraRef.current.takePictureAsync(options);
        const image = await manipulateAsync(imageFile.uri, [{ resize: { width: 480, height: 640 } }], { base64: true });
        const imageData = await fetch(imageFile.uri);
        const blobData = await imageData.blob();
        return {
            'base64': image.base64,
            'type': blobData.type,
        }
    }
    return null;
}

export const getCameraPermission = async (navigation, switchPara = true) => {
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

    if (switchPara) {
        handleCameraPermission();
    }
}