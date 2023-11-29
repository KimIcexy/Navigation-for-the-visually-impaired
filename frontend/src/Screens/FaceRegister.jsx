import * as React from 'react';
import { useState, useRef, useEffect } from 'react';
import { StyleSheet, Text, View, Pressable, Alert, Image } from 'react-native';
import { Camera } from 'expo-camera';
import * as FaceDetector from 'expo-face-detector';

import { TextStyle, TitleStyle, ButtonStyle } from '../Constant/Style.jsx';
import { getImage } from '../Utils/camera.js';
import { createForm } from '../Utils/formData.js';
import { useUser } from '../Hooks/useAuth.js';
import FaceAPI from '../Services/Face_API.js';

const styles = StyleSheet.create({
    container: {
        display: 'flex',
        flex: 1,
    },
    contentContainer: {
        flex: 1,
        justifyContent: 'center',
    },
    welcomeText: [TextStyle.base, {
        fontSize: 20,
        color: '#000000'
    }],
    mainContainer: {
        width: '100%', 
        height: 300
    }
});

const FaceRegister = ({ navigation }) => {
    const { status, user, token } = useUser();

    const [image, setImage] = useState(null); // Valid image, add for confirmation
    const [base64, setBase64] = useState(null); // Base64 image, current image to validate
    const [isCaptured, setIsCaptured] = useState(false); // Check if image is captured to stop capturing

    const cameraRef = useRef(null);

    useEffect(() => {
        const initCamera = async () => {
            const { status } = await Camera.requestCameraPermissionsAsync();
            if (status !== 'granted') {
                Alert.alert('Quyền truy cập camera bị từ chối', 'Vui lòng cấp quyền truy cập camera để sử dụng tính năng đăng nhập bằng mặt người.');
                navigation.navigate('Home');
                return ;
            }
        }
        initCamera();
    }, [])

    const handleFaceDetected = async ({faces}) => {
        if (isCaptured) {
            return ;
        }
        if (faces.length == 1) {
            console.log('Face detected');
            setIsCaptured(true);

            const imageBase64 = await getImage(cameraRef);
            setBase64(imageBase64.base64);
            const formData = createForm(imageBase64);

            // Register face
            let res = null;
            try {
                res = await FaceAPI.valid(formData, token);
            }
            catch (err) {
                console.log(err);
                Alert.alert('Phát hiện khuôn mặt thất bại', err);
                return ;
            }

            const resData = await res.data;

            const imageUri = `data:${imageBase64.type};base64,${resData['image']}`;

            setImage(imageUri);
        }
    }

    const handleRegister = async () => {
        const data = {
            base64: base64,
        }
        const formData = createForm(data);

        let res = null;
        try {
            res = await FaceAPI.register(formData, token);
        }
        catch (err) {
            Alert.alert('Đăng ký thất bại', err);
            return ;
        }

        const resData = await res.data;

        Alert.alert('Đăng ký thành công', 'Khuôn mặt của bạn đã được đăng ký thành công.', [{
            text: 'OK',
            onPress: () => navigation.navigate('Home')
        }]);
    }

    return (
        <View style={styles.container}>
            {/* Title app */}
            <View style={TitleStyle.container}>
                <Text style={TitleStyle.text}>Đăng ký khuôn mặt</Text>
            </View>
            <View style={styles.contentContainer}>
                {image && (
                    <View>
                        <Image source={{uri: image}} style={styles.mainContainer} />
                        <View style={{display: 'flex'}}>
                            <Pressable style={ButtonStyle.container} onPress={handleRegister}>
                                <Text style={ButtonStyle.text}>Xác nhận</Text>
                            </Pressable>
                            <Pressable style={ButtonStyle.container} onPress={() => setImage(null)}>
                                <Text style={ButtonStyle.text}>Chụp lại</Text>
                            </Pressable>
                        </View>
                    </View>
                )}
                {!image && (
                    <View style={{display: 'flex'}}>
                        <Camera 
                            ref={cameraRef}
                            style={styles.mainContainer} 
                            type={Camera.Constants.Type.front}
                            onCameraReady={() => {
                                console.log('Camera ready');
                            }}
                            faceDetectorSettings={{
                                mode: FaceDetector.FaceDetectorMode.fast,
                                detectLandmarks: FaceDetector.FaceDetectorLandmarks.none,
                                runClassifications: FaceDetector.FaceDetectorClassifications.none,
                                minDetectionInterval: 100,
                                tracking: true,
                            }}
                            onFacesDetected={handleFaceDetected}
                        />
                    </View>
                )}
                <View>
                    <Pressable style={ButtonStyle.container} onPress={() => navigation.navigate('Home')}>
                        <Text style={ButtonStyle.text}>Quay lại trang chủ</Text>
                    </Pressable>
                </View>
            </View>
        </View>
    )
}

export default FaceRegister;