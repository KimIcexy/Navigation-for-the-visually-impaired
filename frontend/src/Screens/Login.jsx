import * as React from 'react';
import { Text, View, Button, Pressable, TextInput, StyleSheet } from 'react-native';
import { Formik } from 'formik';

import { TextStyle, TitleStyle, ButtonStyle } from '../Constant/Style.jsx';

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
    return (
        <View style={styles.container}>
            <View style={TitleStyle.container}>
                <Text style={TitleStyle.text}>Đăng nhập</Text>
                <Text style={TitleStyle.text}>Chào mừng trở lại!</Text>
            </View>
            <View style={styles.contentContainer}>
                <Formik
                    initialValues={{username: '', password: ''}}
                    onSubmit={values => console.log(values)}
                >
                    {({handleChange, handleBlur, handleSubmit, values}) => (
                        <View>
                            <TextInput
                                style={styles.textInput}
                                onChangeText={handleChange('username')}
                                onBlur={handleBlur('username')}
                                value={values.username}
                            />
                            <TextInput
                                style={styles.textInput}
                                onChangeText={handleChange('password')}
                                onBlur={handleBlur('password')}
                                value={values.password}
                                secureTextEntry={true}
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