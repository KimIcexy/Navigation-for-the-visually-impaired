import * as React from 'react';
import { StyleSheet, Text, View, Pressable } from 'react-native';

import { TextStyle, TitleStyle, ButtonStyle } from '../Constant/Style.jsx';
import { removeToken, removeUser } from '../Utils/user.js';
import { useUser } from '../Hooks/useAuth.js';

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
            <View style={TitleStyle.container}>
                <Text style={TitleStyle.text}>Ứng dụng điều hướng</Text>
                <Text style={TitleStyle.text}>cho người khiếm thị</Text>
            </View>
            <View style={styles.contentContainer}>
                {
                    status === 'Loading' && (<Text>Loading...</Text>)
                    
                }
                {
                    user == null && (
                        <View>
                            <Pressable style={ButtonStyle.container} onPress={() => navigation.navigate('Login')}>
                                <Text style={ButtonStyle.text}>Đăng nhập</Text>
                            </Pressable>
                            <Pressable style={ButtonStyle.container} onPress={() => navigation.navigate('Register')}>
                                <Text style={ButtonStyle.text}>Đăng ký</Text>
                            </Pressable>
                        </View>
                    )
                }
                {
                    user != null && (
                        <View>
                            <Text style={styles.welcomeText}>Chào mừng {user.username}.</Text>
                            <Pressable style={ButtonStyle.container}>
                                <Text style={ButtonStyle.text}>Điều hướng</Text>
                            </Pressable>
                            <Pressable style={ButtonStyle.container} onPress={handleLogout}>
                                <Text style={ButtonStyle.text}>Đăng xuất</Text>
                            </Pressable>
                        </View>
                    )
                }
            </View>
        </View>
    )
}

export default Home;