import * as React from 'react';
import { useState } from 'react';
import { View } from 'react-native';

import SpeechModal from '../Components/speechModal.jsx';
import NavBar from '../Components/navBar.jsx';

const Screen = ({ navigation, children }) => {
    const [isRecording, setIsRecording] = useState(false);
    
    const handleRecord = () => {
        setIsRecording(!isRecording);
        console.log(isRecording);
    }

    return (
        <View style={{flex: 1}}>
            <NavBar navigation={navigation} handleRecord={handleRecord}/>
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
import LoadingPage from './Loading.jsx';
import FaceDetectionPage from './FaceDetection.jsx';

export const Home = (props) => (<Screen {...props}><HomePage /></Screen>)
export const Login = (props) => (<Screen {...props}><LoginPage /></Screen>)
export const Register = (props) => (<Screen {...props}><RegisterPage /></Screen>)
export const FaceRegister = (props) => (<Screen {...props}><FaceRegisterPage /></Screen>)
export const Loading = (props) => (<Screen {...props}><LoadingPage /></Screen>)
export const FaceDetection = (props) => (<Screen {...props}><FaceDetectionPage /></Screen>)
