import * as React from 'react';
import { Text, View, Button } from 'react-native';

const Register = ({navigation}) => {
    return (
        <View>
            <Text>Register page.</Text>
            <Button
                title='Home'
                onPress={() => navigation.navigate('Home')} />
            <Button
                title='Login'
                onPress={() => navigation.navigate('Login')} />
        </View>
    )
}

export default Register;