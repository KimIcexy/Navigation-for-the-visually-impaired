import * as React from 'react';
import { View, StyleSheet } from 'react-native';
import { useState, useEffect, useRef } from 'react';
import { Camera } from 'expo-camera';
import { io } from 'socket.io-client';

import { getCameraPermission } from '../Utils/camera.js';
import { getToken } from '../Utils/user.js';
import { BACKEND_URL } from '@env'
import { getImage } from '../Utils/camera.js';

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
    }, []);

    getCameraPermission(navigation);

    const [state, setState] = useState(false); // State, true if is sending, false if not sending
    const cameraRef = useRef(null);
    let intervalId;

    // const socket = io(BACKEND_URL, {
    //     transports: ['websocket'],
    //     query: {
    //         token: token,
    //     }
    // });

    const socket = io(BACKEND_URL, { secure: true })

    useEffect(() => {
        socket.on("connect", () => {
            console.log("Connected to socket");
        });
    
        socket.on("disconnect", () => {
            console.log("Disconnected from socket");
        });

        return () => {
            clearInterval(intervalId);
            socket.disconnect();
            setState(false);
        }
    }, []);

    // Continously send image to server
    const sendImageContinously = async () => {
        if (state) {
            return;
        }
        setState(true);
        const image = await getImage(cameraRef);
        console.log("Sending image")
        socket.emit("image", image);
        setState(false);
    }

    const onCameraReady = async () => {
        intervalId = setInterval(async () => {
            sendImageContinously();
        }, 100);
    };

    return (
        <View style = {styles.container}>
            <Camera 
                style={styles.camera} 
                type={Camera.Constants.Type.back} 
                onCameraReady={onCameraReady}
                ref={cameraRef}
            />
        </View>
    )
}

export default Navigating;