import { useState, useRef } from 'react';
import { StyleSheet, View, TextInput, TouchableOpacity, Alert } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import { Audio } from 'expo-av';
import { sendToAWS } from '../../(services)/api/lambda';
import * as FileSystem from 'expo-file-system';

const PRESIGNED_ENDPOINT_URL = 'https://yh8cmasjvk.execute-api.us-west-2.amazonaws.com/prod/get-presigned-url';
interface MessageInputProps {
  username: string;
  onSendText: (text: string, is_user: boolean) => void;
  onSendImage: (uri: string) => void;
  onSendAudio: (uri: string) => void;
}

async function uploadImageToS3(presignedUrl: string, file: string) {
  try {
      const response = await fetch(presignedUrl, {
          method: 'PUT',
          body: file
      });

      if (!response.ok) {
          throw new Error('Failed to upload image to S3');
      }

      console.log('Image uploaded successfully');
  } catch (error) {
      console.error('Error uploading image:', error);
  }
}



export function MessageInput({ username, onSendText, onSendImage, onSendAudio }: MessageInputProps) {
  const [text, setText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const recordingRef = useRef<Audio.Recording | null>(null);

  const handleSendText = async () => {
    if (text.trim()) {

      // data with user message and bool is_image set to false
      const data = {
        message: text.trim(),
        is_image: false,
        timestamp: new Date().toISOString(),
        user_id: username  // Include username in the request
      };
      onSendText(text.trim(), true);
      setText('');
      
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
      // Step 1: Get presigned URL

      const get_presigned_url = async () => {
        const result = await fetch("https://wpusf87tnj.execute-api.us-west-2.amazonaws.com/prod/get-presigned-url")
        const body = await result.json()
        return body["presigned_url"]
      }


      console.log("uri", uri)
      const presignedUrl = await get_presigned_url()
      const imageResponse = await fetch(uri);
      const imageBlob = await imageResponse.blob();

      // Add these debug logs
      console.log('Presigned URL:', presignedUrl);
      console.log('Image blob size:', imageBlob.size);
      console.log('Image blob type:', imageBlob.type);
      // console.log('Image blob:', imageBlob);

      // const file = new File([imageBlob], 'image.jpg', { type: 'image/jpeg' });

      // const file = await fs.readFileSync(uri);

      // const blob = new Blob([file], { type: 'image/jpeg' });
      
      const uploadResponse = await fetch(presignedUrl, {
        method: 'PUT',
        body: imageBlob
      });

      if (!uploadResponse.ok) {
        throw new Error(`Upload failed with status: ${uploadResponse.status}`);
      }

      // Get the public URL from the presigned URL by removing query parameters
      const publicUrl = presignedUrl.split('?')[0];
      onSendImage(publicUrl);
      Alert.alert('Success', 'Image uploaded successfully');

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