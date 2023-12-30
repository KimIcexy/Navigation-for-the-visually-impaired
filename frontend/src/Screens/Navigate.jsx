import * as React from 'react';
import { View, StyleSheet, Alert } from 'react-native';
import { useState, useEffect, useRef } from 'react';
import { Camera } from 'expo-camera';

import { getCameraPermission } from '../Utils/camera.js';
import { getToken } from '../Utils/user.js';
import { getImage } from '../Utils/camera.js';
import NavigateAPI from '../Services/Navigate_API.js'
import { createForm } from '../Utils/formData.js';

const styles = StyleSheet.create({
    container: {
        display: 'flex',
        flex: 1,
    },
    camera: {
        flex: 1,
        position: 'relative'
    },
});

const Navigating = ({ navigation }) => {
    const [token, setToken] = useState(null);

    getCameraPermission(navigation);

    const [state, setState] = useState(false);
    const cameraRef = useRef(null);

    const sendAPI = async () => {
        const imageBase64 = await getImage(cameraRef);
        const formData = createForm(imageBase64);

        let res = null;
        try {
            res = await NavigateAPI.navigate(formData, token);
            return res;
        }
        catch (err) {
            const button = {
                text: 'OK',
                onPress: () => navigation.navigate('Home')
            }
            // Check if err is a string
            const errorMessage = typeof err == 'string' ? err : '';
            Alert.alert('Điều hướng thất bại', errorMessage, [button]);
            console.log(err);
            return false;
        }
    }

    // Continously send image to server
    const sendImageContinously = async () => {
        setState(true);
        const res = await sendAPI();
        setState(false);
        if (res == false) {
            return;
        }
    }

    useEffect(() => {
        if (!state && token != null) {
            sendImageContinously();
        }
    }, [state, token])

    useEffect(() => {
        const getTokenAPI = async () => {
            const token = await getToken();
            setToken(token);
        }
        getTokenAPI();
    }, []);

    return (
        <View style = {styles.container}>
            <Camera 
                style={styles.camera} 
                type={Camera.Constants.Type.back} 
                ref={cameraRef}
            />
        </View>
    )
}

export default Navigating;