import { Modal } from "react-native";
import React, { useEffect, useState } from "react";
import { StyleSheet, Text, View, Pressable } from "react-native";

import { TextStyle, ButtonStyle } from '../Constant/Style.jsx';
import Button from "./button.jsx";

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'rgba(0,0,0,0.2)',
    },
    content: {
        backgroundColor: 'white',
        width: '100%',
        padding: 20,
        borderRadius: 10,
    }
})

const NotImplementModal = ({onCancel}) => {
    return (
        <Modal transparent>
            <View style={styles.container}>
                <View style={styles.content}>
                    <Text style={TextStyle.base}>Chức năng này chưa được cài đặt</Text>
                    <Button text='Đóng' onPress={() => onCancel()} />
                </View>
            </View>
        </Modal>
    )
};

export default NotImplementModal;