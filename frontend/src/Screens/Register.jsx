import * as React from 'react';
import { Text, View, Pressable, TextInput, StyleSheet, Alert } from 'react-native';
import { Formik } from 'formik';

import { TextStyle, TitleStyle, ButtonStyle } from '../Constant/Style.jsx';
import UserAPI from '../Services/User_API.js';

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

const Register = ({navigation}) => {
    const handleRegister = async (values) => {
        let res = null;
        try {
            res = await UserAPI.register(values);
        }
        catch (err) {
            // Trying to catch all error
            if (typeof err == 'string') {
                Alert.alert('Đăng ký thất bại', err);
                return ;
            }
            else {
                Alert.alert('Đăng ký thất bại');
                return ;
            }
        }
        Alert.alert('Đăng ký thành công', 'Vui lòng đăng nhập để tiếp tục', [{text: 'OK', onPress: () => navigation.navigate('Login')}]);
    };
    return (
        <View style={styles.container}>
            <View style={TitleStyle.container}>
                <Text style={TitleStyle.text}>Đăng ký</Text>
            </View>
            <View style={styles.contentContainer}>
                <Formik
                    initialValues={{username: '', email: '', phone: '', password: '', confirmPassword: ''}}
                    onSubmit={handleRegister}
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
                                onChangeText={handleChange('email')}
                                onBlur={handleBlur('email')}
                                value={values.email}
                                placeholder='Email'
                                placeholderTextColor='#000000B2'
                            />
                            <TextInput
                                style={styles.textInput}
                                onChangeText={handleChange('phone')}
                                onBlur={handleBlur('phone')}
                                value={values.phone}
                                placeholder='Số điện thoại'
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
                            <TextInput
                                style={styles.textInput}
                                onChangeText={handleChange('confirmPassword')}
                                onBlur={handleBlur('confirmPassword')}
                                value={values.confirmPassword}
                                secureTextEntry={true}
                                placeholder='Xác nhận mật khẩu'
                                placeholderTextColor='#000000B2'
                            />
                            <Pressable style={ButtonStyle.container} onPress={handleSubmit}>
                                <Text style={ButtonStyle.text}>Đăng ký</Text>
                            </Pressable>
                            <View style={styles.pressContainer}>
                                <Text style={[TextStyle.base, {color: '#000'}]}>Đã có tài khoản? </Text>
                                <Pressable onPress={() => navigation.navigate('Login')}>
                                    <Text style={TextStyle.hyperlink}>Đăng nhập</Text>
                                </Pressable>
                            </View>
                        </View>
                    )}
                </Formik>
            </View>
        </View>
    )
}

export default Register;