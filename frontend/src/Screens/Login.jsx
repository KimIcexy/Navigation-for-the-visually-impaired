import * as React from 'react';
import { useState, useEffect, useRef } from 'react';
import { Text, View, Pressable, TextInput, StyleSheet, Alert } from 'react-native';
import Checkbox from 'expo-checkbox';
import { Formik } from 'formik';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Camera, CameraType } from 'expo-camera';
import * as FaceDetector from 'expo-face-detector';

import { TextStyle, TitleStyle, ButtonStyle } from '../Constant/Style.jsx';
import UserAPI from '../Services/User_API.js';
import { getUser } from '../Utils/user.js';
import { getImage } from '../Utils/camera.js';
import { createForm } from '../Utils/formData.js';
import { useUser } from '../Hooks/useAuth.js';

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
        flexDirection: 'row',
        justifyContent: 'center',
    },
    textInput: {
        marginHorizontal: 30,
        marginVertical: 15,
        paddingVertical: 15,
        paddingHorizontal: 8,
        borderRadius: 10,
        borderWidth: 1,
        borderColor: '#000000',
        borderRadius: 5,
        color: '#000000',
    },
    checkBox: {
        borderWidth: 1,
        borderColor: '#000000',
        borderRadius: 5,
        color: '#000000',
    }
});

const Login = ({navigation}) => {
    const { status, user } = useUser();

    const [isFaceMethod, setIsFaceMethod] = useState(false);
    const [loadCamera, setLoadCamera] = useState(false);
    const [isCaptured, setIsCaptured] = useState(false);

    const cameraRef = useRef(null);
    const username = useRef(null);

    const initFaceLogin = async () => {
        const { status } = await Camera.requestCameraPermissionsAsync();
        if (status !== 'granted') {
            Alert.alert('Quyền truy cập camera bị từ chối', 'Vui lòng cấp quyền truy cập camera để sử dụng tính năng đăng nhập bằng mặt người.');
            setIsFaceMethod(false); // Turn off face login
            return ;
        }
        setLoadCamera(true);
    }

    const handleLogin = async (values) => {
        let res = null;
        try {
            res = await UserAPI.login(values);
        }
        catch (err) {
            Alert.alert('Đăng nhập thất bại', err);
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

    useEffect(() => {
        if (isFaceMethod) {
            // Start everything here
            initFaceLogin();
        }
    }, [isFaceMethod]);

    const handleFaceDetected = async ({faces}) => {
        if (isCaptured) {
            return ;
        }
        if (faces.length == 1) {
            setIsCaptured(true);
            const imageBase64 = await getImage(cameraRef);
            const formData = createForm(imageBase64);
            formData.append('username', username.current);

            let res = null;
            try {
                res = await UserAPI.loginWithFace(formData)
            }
            catch (err) {
                Alert.alert('Đăng nhập thất bại');
                console.log(err)
                return ;
            }
            setIsCaptured(false);
            await AsyncStorage.setItem('token', res['data']['token']);
            await AsyncStorage.setItem('user', JSON.stringify(res['data']['user']));

            const user = await getUser();

            Alert.alert('Đăng nhập thành công', 'Xin chào ' + user.username + '.', [{
                text: 'OK', 
                onPress: () => navigation.replace('Home')
            }]);
        }
    }

    return (
        <View style={styles.container}>
            <View style={TitleStyle.container}>
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
                                style={styles.textInput}
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
                            <View style={{flexDirection: 'row', alignItems: 'center', justifyContent: 'center'}}>
                                <Checkbox 
                                    value={isFaceMethod}
                                    onValueChange={() => {
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
                                            style={styles.textInput}
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
                                        {loadCamera && (
                                            <Camera 
                                                style={{width: '100%', height: 300}} 
                                                type={CameraType.front} 
                                                ref={cameraRef} 
                                                faceDetectorSettings={{
                                                    mode: FaceDetector.FaceDetectorMode.fast,
                                                    detectLandmarks: FaceDetector.FaceDetectorLandmarks.none,
                                                    runClassifications: FaceDetector.FaceDetectorClassifications.none,
                                                    minDetectionInterval: 100,
                                                    tracking: true,
                                                }}
                                                onFacesDetected={handleFaceDetected}
                                            />
                                        )}
                                    </View>
                                )
                            }
                            <Pressable style={ButtonStyle.container} onPress={handleSubmit}>
                                <Text style={ButtonStyle.text}>Đăng nhập</Text>
                            </Pressable>
                            <View style={styles.pressContainer}>
                                <Text style={[TextStyle.base, {color: '#000'}]}>Chưa có tài khoản? </Text>
                                <Pressable onPress={() => navigation.navigate('Register')}>
                                    <Text style={TextStyle.hyperlink}>Đăng ký</Text>
                                </Pressable>
                            </View>
                        </View>
                    )}
                </Formik>
            </View>
        </View>
    )
}

export default Login;