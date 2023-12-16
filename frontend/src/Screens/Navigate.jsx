import * as React from 'react';
import { useState, useEffect, useRef } from 'react';
import { View, StyleSheet, Text } from 'react-native';
import { Camera } from 'expo-camera';

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
    useEffect(() => {
        const getPermission = async () => {
            const { status } = await Camera.requestCameraPermissionsAsync();
            if (status !== 'granted') {
                Alert.alert('Quyền truy cập camera bị từ chối', 'Vui lòng cấp quyền truy cập camera để sử dụng tính năng đăng nhập bằng mặt người.');
                return ;
            }
        }
        getPermission();
    }, []);

    return (
        <View style = {styles.container}>
            <Camera style={styles.camera} type={Camera.Constants.Type.back} />
        </View>
    )
}

export default Navigating;