import { Modal } from "react-native";
import React, { useEffect, useState } from "react";
import { StyleSheet, Text, View, Pressable } from "react-native";
import Voice from "@react-native-voice/voice";
import * as Speech from 'expo-speech';

import { TextStyle, ButtonStyle } from '../Constant/Style.jsx';
import Button from './button.jsx';
import { Keyword } from '../Constant/Command.jsx';
import { useUser } from '../Hooks/useAuth.js';

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
  },
  buttonContainer: {
    alignItems: 'center',
  },
  recordButton: {
    backgroundColor: '#FF5733',
    width: 80,
    height: 80,
    borderRadius: 50,
    padding: 15,
    alignItems: 'center',
    justifyContent: 'center',
  },
  textResult: TextStyle.base + {
    color: '#000000',
  }
})

const SpeechModal = ({onCancel, navigation}) => {
  const { status, user } = useUser();
  const [isRecording, setIsRecording] = useState(false);
  const [results, setResults] = useState([]);
  useEffect(() => {
    Voice.onSpeechResults = onSpeechResults;
  }, []);

  const speechOptions = {
    language: 'vi-VN',
  }

  useEffect(() => {
    console.log(results);
    if (results === undefined || results.length === 0) return;
    // Find first location of each keyword
    const tResult = results[0];
    // Lowercase
    const result = tResult.toLowerCase();
    const location = Keyword.map((keyword) => {
      return result.indexOf(keyword.keyword);
    })
    // 'Remove' the keyword that doesn't appear, set it to a very large number
    location.forEach((value, index) => {
      if (value === -1) location[index] = result.length + 1;
    })
    // Find the keyword that appears first
    const minLocation = Math.min(...location);
    if (minLocation === result.length + 1) {
      Speech.speak('Không tìm thấy lệnh nào', speechOptions);
      return;
    }
    // Find the keyword that appears first
    const index = location.indexOf(minLocation);
    // Get the command
    const command = Keyword[index];
    // Execute the command
    switch (command.type) {
      case 'navigate':
        onCancel();
        if (command.authRank === 1 && user === null) {
          Speech.speak('Bạn cần đăng nhập để thực hiện lệnh này', speechOptions);
          return;
        }
        if (command.authRank === -1 && user !== null) {
          Speech.speak('Bạn cần đăng xuất để thực hiện lệnh này', speechOptions);
          return;
        }
        Speech.speak('Đang chuyển hướng', speechOptions);
        navigation.navigate(command.path);
        break;
      default:
        Speech.speak('Không tìm thấy lệnh nào', speechOptions);
        break;
    }
  }, [results])

  const onSpeechResults = (e) => {
    setResults(e.value);
  }

  const onSpeechStart = async (e) => {
    try {
      setIsRecording(true);
      await Voice.destroy();
      await Voice.start('vi-VN');
      console.log('started');
    }
    catch (e) {
      console.error(e);
    }
  }

  const onSpeechEnd = async (e) => {
    try {
      setIsRecording(false);
      await Voice.stop();
      console.log('stopped');
    }
    catch (e) {
      console.error(e);
    }
  }
  return (
    <Modal transparent>
      <View style={styles.container}>
        <View style={styles.content}>
          <View style={styles.buttonContainer}>
            {isRecording ? (
              <Pressable style={styles.recordButton} onPress={onSpeechEnd}>
                <Text style={ButtonStyle.text}>Dừng lại</Text>
              </Pressable>
            ) : (
              <Pressable style={styles.recordButton} onPress={onSpeechStart}>
                <Text style={ButtonStyle.text}>Ghi âm</Text>
              </Pressable>
            )}
          </View>
          <Text style={TextStyle.base}>{results[0]}</Text>
          <Button text='Hủy' onPress={onCancel}/>
        </View>
      </View>
    </Modal>
  );
};

export default SpeechModal;