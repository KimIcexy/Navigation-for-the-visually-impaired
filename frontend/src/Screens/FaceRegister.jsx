import * as React from 'react';
import { useState, useRef, useEffect } from 'react';
import { StyleSheet, Text, View, Modal, Alert, Image } from 'react-native';
import { Camera } from 'expo-camera';

import { TextStyle, TitleStyle, BoundingBoxStyle } from '../Constant/Style.jsx';
import { getImage } from '../Utils/camera.js';
import { createForm } from '../Utils/formData.js';
import { getToken } from '../Utils/user.js';
import FaceAPI from '../Services/Face_API.js';
import { CameraFaceSettings } from '../Constant/Camera.jsx';
import Button from '../Components/button.jsx';
import { resizeImage } from '../Utils/image.js';
import { PHONE_WIDTH } from '../Constant/Phone.jsx';
import { getCameraPermission } from '../Utils/camera.js';

const FaceRegister = ({ navigation }) => {
    const [token, setToken] = useState(null);
    useEffect(() => {
        const getTokenAPI = async () => {
            const token = await getToken();
            setToken(token);
        }
        getTokenAPI();
    }, []);

    const [image, setImage] = useState(null); // Valid image, add for confirmation
    const [base64, setBase64] = useState(null); // Base64 image, current image to validate
    const [isCaptured, setIsCaptured] = useState(false); // Check if image is captured to stop capturing
    const [isSent, setIsSent] = useState(false); // Check if image is sent to stop sending
    const [detectedFaces, setDetectedFaces] = useState([]); // Detected faces, use for face detection

    const cameraRef = useRef(null);

    useEffect(() => {
        getCameraPermission(navigation);
    }, [])

    const handleFaceDetected = async ({faces}) => {
        setDetectedFaces(faces);
        if ((faces.length == 1) && (!isCaptured)) {
            setIsCaptured(true);

            const sendAPI = async () => {
                const imageBase64 = await getImage(cameraRef);
                setBase64(imageBase64.base64);
                const formData = createForm(imageBase64);

                let res = null;
                try {
                    res = await FaceAPI.valid(formData, token);
                    return res;
                }
                catch (err) {
                    const button = {
                        text: 'OK',
                        onPress: () => setIsCaptured(false)
                    }
                    // Check if err is a string
                    if (typeof err == 'string') {
                        Alert.alert('Phát hiện khuôn mặt thất bại', err, [button]);
                    }
                    else {
                        Alert.alert('Phát hiện khuôn mặt thất bại', '', [button]);
                    }
                    console.log(err);
                    return false;
                }
            }

            const res = await sendAPI();
            setIsCaptured(false);
            if (res == false) {
                return;
            }

            const resData = await res.data;
            const imageResize = await resizeImage(resData, PHONE_WIDTH, 300);

            const imageUri = `data:${resData.type};base64,${imageResize}`;

            setImage(imageUri);
            Alert.alert('Đăng ký bằng khuôn mặt', 'Xác nhận mặt người thành công.');
            setIsCaptured(false);
        }
    }

    const handleRegister = async () => {
        if (isSent) {
            return ;
        }
        setIsSent(true);
        Alert.alert('Đăng ký bằng khuôn mặt', 'Đang xử lý...', []);

        const sendAPI = async () => {
            const data = {
                base64: base64,
            }
            const formData = createForm(data);

            let res = null;
            try {
                res = await FaceAPI.register(formData, token);
                return res;
            }
            catch (err) {
                if (typeof err == 'string') {
                    Alert.alert('Phát hiện khuôn mặt thất bại', err);
                }
                else {
                    Alert.alert('Phát hiện khuôn mặt thất bại');
                }
                console.log(err);
                return ;
            }
        }

        const res = await sendAPI();
        setIsSent(false);
        if (res == false) {
            return;
        }
        
        const resData = await res.data;

        Alert.alert('Đăng ký thành công', 'Khuôn mặt của bạn đã được đăng ký thành công.', [{
            text: 'OK',
            onPress: () => navigation.navigate('Home')
        }]);
    }

    const faceBoundingBox = () => {
        if (detectedFaces.length === 0) return ;
        return detectedFaces.map((face, index) => {
            if (face.bounds === undefined) return ;
            const {origin, size} = face.bounds;
            const {x, y} = origin;
            const {width, height} = size;
            return (
                <View
                    key={index}
                    style={BoundingBoxStyle(x, y, width, height)}
                />
            )
        })
    }

    return (
        <View style={styles.container}>
            {isCaptured && <Modal transparent />}
            <View style={TitleStyle.container}>
                <Text style={TitleStyle.text}>Đăng ký khuôn mặt</Text>
            </View>
            <View style={styles.contentContainer}>
                {image && (
                    <View>
                        <Image source={{uri: image}} style={styles.mainContainer} />
                        <View style={{display: 'flex'}}>
                            <Button text='Xác nhận' onPress={handleRegister}/>
                            <Button text='Chụp lại' onPress={() => setImage(null)}/>
                        </View>
                    </View>
                )}
                {!image && (
                    <View style={{display: 'flex'}}>
                        <Camera 
                            ref={cameraRef}
                            style={styles.mainContainer} 
                            type={Camera.Constants.Type.front}
                            faceDetectorSettings={CameraFaceSettings}
                            onFacesDetected={handleFaceDetected}
                        />
                        {faceBoundingBox()}
                    </View>
                )}
                <View>
                    <Button text='Quay lại trang chủ' onPress={() => navigation.navigate('Home')}/>
                </View>
            </View>
        </View>
    )
}

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

export default FaceRegister;