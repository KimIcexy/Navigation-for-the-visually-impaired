import * as React from 'react';
import { useState, useEffect } from 'react';
import { Text, View, Pressable, TextInput, StyleSheet, Alert } from 'react-native';
import { Formik } from 'formik';
import EncryptedStorage from 'react-native-encrypted-storage';

import { TextStyle, TitleStyle, ButtonStyle } from '../Constant/Style.jsx';
import UserAPI from '../Services/User_API.js';
import { getUser } from '../Utils/user.js';
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
});

const Login = ({navigation}) => {
    const { status, user } = useUser();
    if ((status === 'Done') && (user != null)) {
        navigation.replace('Home');
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
        console.log(res);
        await EncryptedStorage.setItem('token', res['data']['token']);
        await EncryptedStorage.setItem('user', JSON.stringify(res['data']['user']));

        const user = await getUser();

        Alert.alert('Đăng nhập thành công', 'Xin chào ' + user.username + '.', [{
            text: 'OK', 
            onPress: () => navigation.replace('Home')
        }]);
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
                    {({handleChange, handleBlur, handleSubmit, values}) => (
                        <View>
                            <TextInput
                                style={styles.textInput}
                                onChangeText={handleChange('username')}
                                onBlur={handleBlur('username')}
                                value={values.username}
                                placeholder='Tên đăng nhập'
                                placeholderTextColor='#000000B2'
                            />
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