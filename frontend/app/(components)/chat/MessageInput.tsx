import { useState, useRef } from 'react';
import { StyleSheet, View, TextInput, TouchableOpacity, Alert } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import { Audio } from 'expo-av';
import { sendImageToChat, sendToAWS, createCreator } from '../../(services)/api/lambda';

const PRESIGNED_ENDPOINT_URL = 'https://yh8cmasjvk.execute-api.us-west-2.amazonaws.com/prod/get-presigned-url/{user_id}/{creator_id}';
const GET_CREATOR_ID_URL = 'https://yh8cmasjvk.execute-api.us-west-2.amazonaws.com/prod/get-active-creator/{user_id}';


interface MessageInputProps {
  username: string;
  is_new_conversation: boolean;
  onSendText: (text: string, is_user: boolean) => void;
  onSendImage: (uri: string) => void;
  onSendAudio: (uri: string) => void;
}

export function MessageInput({ username, is_new_conversation, onSendText, onSendImage, onSendAudio }: MessageInputProps) {
  const [text, setText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const recordingRef = useRef<Audio.Recording | null>(null);

 

  const getCreatorId = async () => {
    const result = await fetch(GET_CREATOR_ID_URL.replace('{user_id}', username))
    const body = await result.json()
    console.log("get active creator result: ", body)
    return body["offer_creator"]["id"];
  }

  const handleSendText = async () => {
    if (text.trim()) {
      onSendText(text.trim(), true);
      setText('');

      // if it is the first message, create a new creator
      let creator_id = "";
      if (is_new_conversation) {
        console.log("Creating new creator for user: ", username)
        const data = {
          user_id: username
        };
        creator_id = (await createCreator(data)).creator_id!;
      }
      else {
        creator_id = await getCreatorId();
      }

      console.log("creator_id: ", creator_id)

      const data = {
        message: text.trim(),
        is_image: false,
        timestamp: new Date().toISOString(),
        user_id: username,
        creator_id: creator_id
      };
      
      try {
        // Send message to Lambda
        const response = await sendToAWS(data);
        onSendText(response.message, false);
      } catch (error) {
        console.error('Error sending message to Lambda:', error);
        Alert.alert('Error', 'Failed to send message');
      }
    }
  };

  const handleImagePick = async () => {
    try {
      const result = await ImagePicker.launchCameraAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        quality: 0.8,
      });

      if (!result.canceled && result.assets[0]) {
        await uploadImage(result.assets[0].uri);
      }
    } catch (error) {
      console.error('Error picking image:', error);
      Alert.alert('Error', 'Failed to capture image');
    }
  };

  const uploadImage = async (uri: string) => {
    try {
      onSendImage(uri);


      const creator_id = await getCreatorId();

      // get presigned url  
      console.log("getting presigned url for user: ", username, " and creator: ", creator_id)
      const get_presigned_url = async () => {
        const result = await fetch(PRESIGNED_ENDPOINT_URL.replace('{user_id}', username).replace('{creator_id}', creator_id))
        const body = await result.json()
        return body["presigned_url"]
      }


      const presignedUrl = await get_presigned_url()
      console.log("presignedUrl: ", presignedUrl)
        
      const imageResponse = await fetch(uri);
      const imageBlob = await imageResponse.blob();
      
      const uploadResponse = await fetch(presignedUrl, {
        method: 'PUT',
        body: imageBlob
      });

      if (!uploadResponse.ok) {
        throw new Error(`Upload failed with status: ${uploadResponse.status}`);
      }

      // send image to chat
      const data = {
        message: "",
        user_id: username,  // Include username in the request
        creator_id: creator_id
      };
      console.log("sending image to chat: ", data)
      const response = await sendImageToChat(data);
      console.log("response after sending image to chat: ", response)
      onSendText(response["message"], false);

    } catch (error) {
      console.error('Upload error:', error);
      Alert.alert('Error', 'Failed to upload image');
    }
  };

  const startRecording = async () => {
    try {
      await Audio.requestPermissionsAsync();
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      const recording = new Audio.Recording();
      await recording.prepareToRecordAsync(Audio.RecordingOptionsPresets.HIGH_QUALITY);
      await recording.startAsync();
      recordingRef.current = recording;
      setIsRecording(true);
    } catch (error) {
      console.error('Failed to start recording:', error);
    }
  };

  const stopRecording = async () => {
    try {
      if (!recordingRef.current) return;
      
      await recordingRef.current.stopAndUnloadAsync();
      const uri = recordingRef.current.getURI();
      setIsRecording(false);
      
      if (uri) {
        onSendAudio(uri);
      }
    } catch (error) {
      console.error('Failed to stop recording:', error);
    }
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.button} onPress={handleImagePick}>
        <MaterialIcons name="camera-alt" size={24} color="#007AFF" />
      </TouchableOpacity>
      
      <TouchableOpacity 
        style={styles.button} 
        onPress={isRecording ? stopRecording : startRecording}
      >
        <MaterialIcons 
          name={isRecording ? "stop" : "mic"} 
          size={24} 
          color={isRecording ? "#FF3B30" : "#007AFF"} 
        />
      </TouchableOpacity>

      <TextInput
        style={styles.input}
        value={text}
        onChangeText={setText}
        placeholder="Type your message..."
        multiline
      />

      <TouchableOpacity style={styles.button} onPress={handleSendText}>
        <MaterialIcons name="send" size={24} color="#007AFF" />
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 8,
    backgroundColor: 'white',
    borderTopWidth: 1,
    borderTopColor: '#eee',
  },
  input: {
    flex: 1,
    marginHorizontal: 8,
    padding: 8,
    maxHeight: 100,
    backgroundColor: '#f5f5f5',
    borderRadius: 20,
    fontSize: 16,
  },
  button: {
    padding: 8,
  },
});

export default MessageInput; 