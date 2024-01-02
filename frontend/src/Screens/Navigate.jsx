import * as React from 'react';
import { View, StyleSheet, Alert, Text } from 'react-native';
import { useState, useEffect, useRef } from 'react';
import { Camera } from 'expo-camera';

import { getCameraPermission } from '../Utils/camera.js';
import { getToken } from '../Utils/user.js';
import { getImage } from '../Utils/camera.js';
import NavigateAPI from '../Services/Navigate_API.js'
import { createForm } from '../Utils/formData.js';
import { BoundingBoxStyle } from '../Constant/Style.jsx';
import { PHONE_HEIGHT, PHONE_WIDTH } from '../Constant/Phone.jsx';
import * as Speech from 'expo-speech';

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

    const [obstacles, setObstacles] = useState([]);
    const [path, setPath] = useState([]);

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
                // onPress: () => navigation.navigate('Home')
            }
            // Check if err is a string
            const errorMessage = typeof err == 'string' ? err : '';
            Alert.alert('Điều hướng thất bại', errorMessage, [button]);
            console.log(err);
            return false;
        }
    }

    const speechOptions = {
        language: 'vi-VN',
    }

    // Continously send image to server
    const sendImageContinously = async () => {
        setState(true);
        const res = await sendAPI();
        setState(false);
        if (res == false) {
            return;
        }
        const { data } = res;
        setObstacles(data?.obstacles);
        setPath(data?.path);
        // Speak all the diẻctions
        for (i = 0; i < data?.directions.length; i++) {
            Speech.speak(data?.directions[i], speechOptions);
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

    const drawObstacles = () => {
        if (obstacles.length == 0) {
            return ;
        }
        return obstacles.map((obstacle, index) => {
            const coor = obstacle[0];
            const name = obstacle[1];
            // Scaling here
            const x = coor[0] * (PHONE_WIDTH / 480);
            const y = coor[1] * (PHONE_HEIGHT / 640);
            const x1 = coor[2] * (PHONE_WIDTH / 480);
            const y1 = coor[3] * (PHONE_HEIGHT / 640);
            return (
                <View 
                    key={index}
                    style={BoundingBoxStyle(x, y, x1-x, y1-y)}
                >
                    <Text style={{color: 'white', fontSize: 15}}>{name}</Text>
                </View>
            )
        })
    }

    const drawPath = () => {
        if (path.length == 0) {
            return ;
        }
        return path.map((point, index) => {
            const x = point[0] * (PHONE_WIDTH / 480);
            const y = point[1] * (PHONE_HEIGHT / 640);
            return (
                <View 
                    key={index}
                    style={{
                        position: 'absolute',
                        left: x,
                        top: y,
                        width: 10,
                        height: 10,
                        backgroundColor: 'green',
                        opacity: 0.5
                    }}
                />
            )
        })
    }

    return (
        <View style = {styles.container}>
            <Camera 
                style={styles.camera} 
                type={Camera.Constants.Type.back} 
                ref={cameraRef}
            />
            {drawPath()}
            {drawObstacles()}
        </View>
    )
}

export default Navigating;