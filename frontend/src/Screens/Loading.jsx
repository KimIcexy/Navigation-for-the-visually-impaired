import * as React from 'react';
import { View, Text, StyleSheet } from 'react-native';

import { TitleStyle } from '../Constant/Style.jsx';

const styles = StyleSheet.create({
    container: {
        display: 'flex',
        flex: 1,
        justifyContent: 'center',
    },
});

const Loading = () => {
    return (
        <View style={styles.container}>
            <Text style={TitleStyle.text}>Loading...</Text>
        </View>
    )
}

export default Loading;