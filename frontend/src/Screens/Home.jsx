import * as React from 'react';
import { Text, View, Button } from 'react-native';

const Home = ({ navigation }) => {
    return (
        <View>
            <Text>Home page.</Text>
            <Button
                title='Login'
                onPress={() => navigation.navigate('Login')} />
            <Button
                title='Register'
                onPress={() => navigation.navigate('Register')} />
        </View>
    )
}

export default Home;