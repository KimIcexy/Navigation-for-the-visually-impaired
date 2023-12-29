import * as React from 'react';
import { StyleSheet, Text, View, Pressable } from 'react-native';

import { TextStyle, TitleStyle } from '../Constant/Style.jsx';
import { removeToken, removeUser } from '../Utils/user.js';
import { useUser } from '../Hooks/useAuth.js';
import Button from '../Components/button.jsx';

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
    }]
});

const Home = ({ navigation }) => {
    const { status, user } = useUser();

    const handleLogout = () => {
        removeUser();
        removeToken();
        navigation.replace('Home');
    }

    return (
        <View style={styles.container}>
            {/* Title app */}
            <View style={TitleStyle.container} accessible>
                <Text style={TitleStyle.text}>Ứng dụng điều hướng</Text>
                <Text style={TitleStyle.text}>cho người khiếm thị</Text>
            </View>
            <View style={styles.contentContainer}>
                {
                    user == null && (
                        <View>
                            <Button text="Đăng nhập" onPress={() => navigation.navigate('Login')} />
                            <Button text="Đăng ký" onPress={() => navigation.navigate('Register')} />
                        </View>
                    )
                }
                {
                    user != null && (
                        <View>
                            <Text style={styles.welcomeText}>Chào mừng {user.username}.</Text>
                            <Button text="Điều hướng" onPress={() => navigation.navigate('Navigation')} />
                            <Button text="Đăng ký mặt người" onPress={() => navigation.navigate('FaceRegister')} />
                            <Button text="Đăng xuất" onPress={handleLogout} />
                        </View>
                    )
                }
                <Button text="Testing" onPress={() => navigation.navigate('FaceDetection')} />
            </View>
        </View>
    )
}

export default Home;