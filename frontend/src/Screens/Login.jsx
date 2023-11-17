import * as React from 'react';
import { Text, View, Button } from 'react-native';

const Login = ({navigation}) => {
    return (
        <View>
            <Text>Login page.</Text>
            <Button
                title='Home'
                onPress={() => navigation.navigate('Home')} />
            <Button
                title='Register'
                onPress={() => navigation.navigate('Register')} />
        </View>
    )
}

export default Login;