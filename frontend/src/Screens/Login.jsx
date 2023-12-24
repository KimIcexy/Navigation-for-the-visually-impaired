import * as React from 'react';
import { useState, useRef } from 'react';
import { Text, View, Pressable, TextInput, StyleSheet, Alert, Modal } from 'react-native';
import Checkbox from 'expo-checkbox';
import { Formik } from 'formik';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Camera } from 'expo-camera';

import { TextStyle, TitleStyle, InputStyle, BoundingBoxStyle } from '../Constant/Style.jsx';
import UserAPI from '../Services/User_API.js';
import { getUser } from '../Utils/user.js';
import { getImage } from '../Utils/camera.js';
import { createForm } from '../Utils/formData.js';
import { CameraFaceSettings } from '../Constant/Camera.jsx';
import Button from '../Components/button.jsx';
import { getCameraPermission } from '../Utils/camera.js';

const Login = ({navigation}) => {
    const [isFaceMethod, setIsFaceMethod] = useState(false);
    const [isCaptured, setIsCaptured] = useState(false);
    const [detectedFaces, setDetectedFaces] = useState([]);

    const cameraRef = useRef(null);
    const username = useRef(null);

    const handleLogin = async (values) => {
        let res = null;
        try {
            res = await UserAPI.login(values);
        }
        catch (err) {
            if (typeof err == 'string') {
                Alert.alert('Đăng nhập thất bại', err);
            }
            else {
                Alert.alert('Đăng nhập thất bại');
            }
            console.log(err);
            return ;
        }
        await AsyncStorage.setItem('token', res['data']['token']);
        await AsyncStorage.setItem('user', JSON.stringify(res['data']['user']));

        const user = await getUser();

        Alert.alert('Đăng nhập thành công', 'Xin chào ' + user.username + '.', [{
            text: 'OK', 
            onPress: () => navigation.replace('Home')
        }]);
    }

    getCameraPermission(navigation, isFaceMethod);

    const handleFaceDetected = async ({faces}) => {
        setDetectedFaces(faces);
        if ((faces.length == 1) && (!isCaptured)) {
            setIsCaptured(true);

            const sendAPI = async () => {
                const imageBase64 = await getImage(cameraRef);
                const formData = createForm(imageBase64);
                formData.append('username', username.current);
                
                let res = null;
                try {
                    res = await UserAPI.loginWithFace(formData)
                    return res
                }
                catch (err) {
                    const button = {text: 'OK', onPress: () => setIsCaptured(false)};
                    if (typeof err == 'string') {
                        Alert.alert('Đăng nhập bằng khuôn mặt thất bại', err, [button]);
                    }
                    else {
                        Alert.alert('Đăng nhập bằng khuôn mặt thất bại', 'Vui lòng thử lại.', [button]);
                    }
                    return false;
                }
            }
            const res = await sendAPI();
            if (res == false) {
                return ;
            }
            await AsyncStorage.setItem('token', res['data']['token']);
            await AsyncStorage.setItem('user', JSON.stringify(res['data']['user']));

            const user = await getUser();

            Alert.alert('Đăng nhập thành công', 'Xin chào ' + user.username + '.', [{
                text: 'OK', 
                onPress: () => navigation.replace('Home')
            }]);
        }
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
            <View style={TitleStyle.container} accessible>
                <Text style={TitleStyle.text}>Đăng nhập</Text>
                <Text style={TitleStyle.text}>Chào mừng trở lại!</Text>
            </View>
            <View style={styles.contentContainer}>
                <Formik
                    initialValues={{username: '', password: ''}}
                    onSubmit={handleLogin}
                >
                    {({handleChange, handleBlur, handleSubmit, values, setFieldValue, setFieldTouched}) => (
                        <View>
                            <TextInput
                                style={InputStyle}
                                onChangeText={(val) => {
                                    setFieldValue('username', val)
                                    setFieldTouched('username', true, false);
                                    username.current = val;
                                }
                                    }
                                onBlur={handleBlur('username')}
                                value={values.username}
                                placeholder='Tên đăng nhập'
                                placeholderTextColor='#000000B2'
                            />
                            {/* Change login method */}
                            <View style={{flexDirection: 'row', alignItems: 'center', justifyContent: 'center'}} accessible>
                                <Checkbox
                                    style={{marginRight: 5}}
                                    value={isFaceMethod}
                                    onValueChange={async () => {
                                        setIsFaceMethod(!isFaceMethod);
                                    }}
                                    tintColors={{true: '#0E64D2', false: '#000000'}}
                                />
                                <Text style={TextStyle.base}>Sử dụng đăng nhập bằng mặt người</Text>
                            </View>
                            {
                                !isFaceMethod && (
                                    <View>
                                        <TextInput
                                            style={InputStyle}
                                            onChangeText={handleChange('password')}
                                            onBlur={handleBlur('password')}
                                            value={values.password}
                                            secureTextEntry={true}
                                            placeholder='Mật khẩu'
                                            placeholderTextColor='#000000B2'
                                        />
                                        <View style={styles.pressContainer}>
                                            <Pressable>
                                                <Text style={TextStyle.hyperlink}>Quên mật khẩu?</Text>
                                            </Pressable>
                                        </View>
                                    </View>
                                )
                            }
                            {
                                isFaceMethod && (
                                    <View style={{paddingVertical: 15}}>
                                        <View>
                                            <Camera 
                                                style={{width: '100%', height: 300}} 
                                                type={Camera.Constants.Type.front} 
                                                ref={cameraRef} 
                                                faceDetectorSettings={CameraFaceSettings}
                                                onFacesDetected={handleFaceDetected}
                                            />
                                            {faceBoundingBox()}
                                        </View>
                                    </View>
                                )
                            }
                            <Button text='Đăng nhập' onPress={handleSubmit}/>
                            <View style={styles.pressContainer} accessible>
                                <Pressable onPress={() => navigation.navigate('Register')} accessible>
                                    <Text style={TextStyle.hyperlink}>Chưa có tài khoản? Đăng ký</Text>
                                </Pressable>
                            </View>
                        </View>
                    )}
                </Formik>
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
        marginTop: 75,
    },
    pressContainer: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    checkBox: {
        borderWidth: 1,
        borderColor: '#000000',
        borderRadius: 5,
        color: '#000000',
    }
});

export default Login;