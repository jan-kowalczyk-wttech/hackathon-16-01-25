import { useState, useRef } from 'react';
import { StyleSheet, View, TextInput, TouchableOpacity, Alert } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import { Audio } from 'expo-av';
import * as FileSystem from 'expo-file-system';

const API_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:3000';

interface MessageInputProps {
  onSendText: (text: string) => void;
  onSendImage: (uri: string) => void;
  onSendAudio: (uri: string) => void;
}

export function MessageInput({ onSendText, onSendImage, onSendAudio }: MessageInputProps) {
  const [text, setText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const recordingRef = useRef<Audio.Recording | null>(null);

  const handleSendText = () => {
    if (text.trim()) {
      onSendText(text.trim());
      setText('');
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
      // First try to upload to server
      const formData = new FormData();
      formData.append('image', {
        uri,
        type: 'image/jpeg',
        name: 'photo.jpg',
      } as any);

      const response = await fetch(`${API_URL}/api/chat/upload`, {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (!response.ok) {
        throw new Error('Server upload failed');
      }

      const { imageUrl } = await response.json();
      onSendImage(imageUrl);

    } catch (error) {
      console.warn('Server upload failed, using mock storage:', error);
      
      // Fallback to mock storage if server is unavailable
      try {
        // Copy image to app's local storage as a mock solution
        const fileName = `${Date.now()}.jpg`;
        const newUri = FileSystem.documentDirectory + fileName;
        await FileSystem.copyAsync({ from: uri, to: newUri });
        
        onSendImage(newUri);
      } catch (mockError) {
        console.error('Mock storage failed:', mockError);
        Alert.alert('Error', 'Failed to save image');
      }
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