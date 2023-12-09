import { Modal } from "react-native";
import React, { useEffect, useState } from "react";
import { StyleSheet, Text, View, Pressable } from "react-native";
import Voice, {
  SpeechRecognizedEvent,
  SpeechResultsEvent,
  SpeechErrorEvent,
} from "@react-native-voice/voice";

import { TextStyle, TitleStyle, ButtonStyle } from '../Constant/Style.jsx';

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

const SpeechModal = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [results, setResults] = useState([]);
  useEffect(() => {
    Voice.onSpeechResults = onSpeechResults;
  }, []);

  const onSpeechResults = (e) => {
    console.log(e);
    setResults(e.value);
  }

  const onSpeechStart = async (e) => {
    try {
      setIsRecording(true);
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
          <Pressable style={ButtonStyle.container}>
            <Text style={ButtonStyle.text}>Hủy</Text>
          </Pressable>
        </View>
      </View>
    </Modal>
  );
};

export default SpeechModal;