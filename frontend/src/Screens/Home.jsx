import * as React from 'react';
import { StyleSheet, Text, View, Pressable } from 'react-native';

import { TextStyle, TitleStyle, ButtonStyle } from '../Constant/Style.jsx';

const styles = StyleSheet.create({
    container: {
        display: 'flex',
        flex: 1,
    },
    contentContainer: {
        flex: 1,
        justifyContent: 'center',
    },
});

const Home = ({ navigation }) => {
    return (
        <View style={styles.container}>
            {/* Title app */}
            <View style={TitleStyle.container}>
                <Text style={TitleStyle.text}>Ứng dụng điều hướng</Text>
                <Text style={TitleStyle.text}>cho người khiếm thị</Text>
            </View>
            <View style={styles.contentContainer}>
                <Pressable style={ButtonStyle.container} onPress={() => navigation.navigate('Login')}>
                    <Text style={ButtonStyle.text}>Đăng nhập</Text>
                </Pressable>
                <Pressable style={ButtonStyle.container} onPress={() => navigation.navigate('Register')}>
                    <Text style={ButtonStyle.text}>Đăng ký</Text>
                </Pressable>
            </View>
        </View>
    )
}

export default Home;