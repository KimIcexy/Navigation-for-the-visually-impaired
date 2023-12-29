import * as React from 'react';
import { View, StyleSheet } from 'react-native';
import { useState, useEffect } from 'react';

import { getCameraPermission } from '../Utils/camera.js';
import { getToken } from '../Utils/user.js';

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
    useEffect(() => {
        const getTokenAPI = async () => {
            const token = await getToken();
            setToken(token);
        }
        getTokenAPI();
        start();
    }, []);

    getCameraPermission(navigation);

    return (
        <View style = {styles.container}>
            <Camera style = {styles.camera} type = {Camera.Constants.Type.back} />
        </View>
    )
}

export default Navigating;