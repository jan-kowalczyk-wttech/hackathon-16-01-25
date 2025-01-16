import { useState, useEffect } from 'react';
import { StyleSheet, View, FlatList, Text, TouchableOpacity } from 'react-native';
import { MessageInput } from '../../(components)/chat/MessageInput';
import { MessageBubble } from '../../(components)/chat/MessageBubble';
import AsyncStorage from '@react-native-async-storage/async-storage';


interface Message {
  id: string;
  type: 'text' | 'image' | 'audio';
  content: string;
  timestamp: string;
  isUser: boolean;
}

export default function ChatScreen() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [username, setUsername] = useState<string>('');
  const [is_new_conversation, setIsNewConversation] = useState<boolean>(true);

  useEffect(() => {
    loadUsername();
  }, []);

  const loadUsername = async () => {
    try {
      const savedUsername = await AsyncStorage.getItem('username');
      if (savedUsername) {
        setUsername(savedUsername);
      }
    } catch (error) {
      console.error('Error loading username:', error);
    }
  };

  const addMessage = async (type: 'text' | 'image' | 'audio', content: string, is_user: boolean) => {
    console.log("adding message: ", content)
    setIsNewConversation(false);
    const newMessage: Message = {
      id: Date.now().toString(),
      type,
      content,
      timestamp: new Date().toLocaleTimeString(),
      isUser: is_user,
    };
    setMessages(prevMessages => [newMessage, ...prevMessages]);
  };

  const startNewConversation = async () => {
    try {
      console.log("Starting new conversation")
      setMessages([]);
      setIsNewConversation(true);
    } catch (error) {
      console.error('Error creating creator:', error);
    }
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity 
        style={styles.newChatButton} 
        onPress={startNewConversation}
      >
        <Text style={styles.newChatButtonText}>New Conversation</Text>
      </TouchableOpacity>
      
      <FlatList
        data={messages}
        renderItem={({ item }) => (
          <MessageBubble
            type={item.type}
            content={item.content}
            timestamp={item.timestamp}
            isUser={item.isUser}
          />
        )}
        keyExtractor={item => item.id}
        inverted
        style={styles.list}
      />
      <MessageInput
        username={username}
        is_new_conversation={is_new_conversation}
        onSendText={(text, is_user) => addMessage('text', text, is_user)}
        onSendImage={(uri) => addMessage('image', uri, true)}
        onSendAudio={(uri) => addMessage('audio', uri, true)}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  list: {
    flex: 1,
  },
  newChatButton: {
    backgroundColor: '#007AFF',
    padding: 12,
    margin: 10,
    borderRadius: 8,
    alignItems: 'center',
  },
  newChatButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
}); 