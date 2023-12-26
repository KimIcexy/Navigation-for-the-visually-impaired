import * as React from 'react';
import { View, StyleSheet, Text } from 'react-native';
import { Camera } from 'expo-camera';

import { getCameraPermission } from '../Utils/camera.js';

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
    getCameraPermission(navigation);

    return (
        <View style = {styles.container}>
            <Camera style={styles.camera} type={Camera.Constants.Type.back} />
        </View>
    )
}

export default Navigating;