import { useEffect } from 'react';
import { Alert } from 'react-native';
import { Camera } from 'expo-camera';
import * as Linking from 'expo-linking';

export const useCameraPermission = (navigation) => {
    useEffect(() => {
        const { status } = Camera.requestCameraPermissionsAsync();
        if (status === null || status === 'granted') {
            return ;
        }
        else {
            Alert.alert(
                "Permission Denied",
                "Please allow camera permission to use this feature",
                [
                    {
                        text: "Cancel",
                        onPress: () => navigation.navigate('Home'),
                    },
                    { text: "OK", onPress: () => Linking.openSettings()}
                ],
            );
        }
    }, [status])

    return ;

}