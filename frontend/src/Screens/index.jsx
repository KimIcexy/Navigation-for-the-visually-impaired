import * as React from 'react';
import { useState } from 'react';
import { View, StyleSheet, Pressable, Text } from 'react-native';
import { Ionicons } from '@expo/vector-icons'; 

import SpeechModal from '../Components/speechModal.jsx';

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

const Screen = ({ navigation, children }) => {
    const [isRecording, setIsRecording] = useState(false);

    const handleRecord = () => {
        setIsRecording(!isRecording);
        console.log(isRecording);
    }

    return (
        <View style={{flex: 1}}>
            <View style={styles.navBarContainer}>
                <Pressable style={styles.buttonContainer} onPress={() => navigation.navigate('Home')}>
                    <Ionicons name="home" size={30} color="white" />
                </Pressable>
                <Pressable style={styles.buttonContainer} onPress={handleRecord}>
                    <Ionicons name="mic" size={30} color="white" />
                </Pressable>
                {/* Setting, TODO */}
                <Pressable style={styles.buttonContainer}> 
                    <Ionicons name="settings" size={30} color="white" />
                </Pressable>
            </View>
            {React.Children.map(children, child => React.cloneElement(child, {navigation}))}
            {isRecording && <SpeechModal onCancel={handleRecord} navigation={navigation}/>}
        </View>
    )
}

// Export all screens here
import HomePage from './Home.jsx';
import LoginPage from './Login.jsx';
import RegisterPage from './Register.jsx';
import FaceRegisterPage from './FaceRegister.jsx';

export const Home = (props) => (<Screen {...props}><HomePage /></Screen>)
export const Login = (props) => (<Screen {...props}><LoginPage /></Screen>)
export const Register = (props) => (<Screen {...props}><RegisterPage /></Screen>)
export const FaceRegister = (props) => (<Screen {...props}><FaceRegisterPage /></Screen>)

