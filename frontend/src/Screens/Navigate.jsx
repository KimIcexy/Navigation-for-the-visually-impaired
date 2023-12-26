import * as React from 'react';
import { View, StyleSheet, Text } from 'react-native';
import { useState, useEffect } from 'react';
import { Camera } from 'expo-camera';
import { mediaDevices, RTCView } from 'react-native-webrtc';

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

    const [stream, setStream] = useState(null);

    const start = async () => {
        if (!stream) {
            let s = null;
            try {
                s = await mediaDevices.getUserMedia({ video: {
                    facingMode: 'user'
                }});
                // Can't seem to set the back camera, so this will do for now.
                s.getVideoTracks().forEach((track) => {
                    track._switchCamera()
                })
                setStream(s);
            }
            catch (err) {
                console.log(err)
            }
        }
    }

    return (
        <View style = {styles.container}>
            {stream && <RTCView style={styles.camera} streamURL={stream.toURL()} />}
        </View>
    )
}

export default Navigating;