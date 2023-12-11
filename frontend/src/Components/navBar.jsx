import * as React from 'react';
import { View, StyleSheet, Pressable, Text } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const styles = StyleSheet.create({
    navBarContainer: {
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '50',
        backgroundColor: '#0E64D2',
        display: 'flex',
        flexDirection: 'row',
        borderRadius: 5,
        justifyContent: 'space-between',
    },
    buttonContainer: {
        padding: 5,
    },
})
const NavBar = ({ navigation, handleRecord }) => {
    return (
        <View style={styles.navBarContainer}>
            <Pressable 
                style={styles.buttonContainer} 
                onPress={() => navigation.navigate('Home')} 
                accessibilityLabel='Trang chủ'
            >
                <Ionicons name="home" size={30} color="white" />
            </Pressable>
            <Pressable 
                style={styles.buttonContainer} 
                onPress={handleRecord}
                accessibilityLabel='Ghi âm'
            >
                <Ionicons name="mic" size={30} color="white" />
            </Pressable>
            {/* Setting, TODO */}
            <Pressable 
                style={styles.buttonContainer}
                accessibilityLabel='Cài đặt'
            > 
                <Ionicons name="settings" size={30} color="white" />
            </Pressable>
        </View>
    )
};

export default NavBar;