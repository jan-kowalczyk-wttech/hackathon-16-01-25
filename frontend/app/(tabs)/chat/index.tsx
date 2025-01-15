import { useState } from 'react';
import { StyleSheet, View, FlatList } from 'react-native';
import { MessageInput } from '../../(components)/chat/MessageInput';
import { MessageBubble } from '../../(components)/chat/MessageBubble';

interface Message {
  id: string;
  type: 'text' | 'image' | 'audio';
  content: string;
  timestamp: string;
  isUser: boolean;
}

export default function ChatScreen() {
  const [messages, setMessages] = useState<Message[]>([]);

  const addMessage = (type: 'text' | 'image' | 'audio', content: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      type,
      content,
      timestamp: new Date().toLocaleTimeString(),
      isUser: true,
    };

    setMessages(prevMessages => [newMessage, ...prevMessages]);

    // Simulate sending to server
    setTimeout(() => {
      const response: Message = {
        id: (Date.now() + 1).toString(),
        type: 'text',
        content: 'Your offer has been received. We will review it shortly.',
        timestamp: new Date().toLocaleTimeString(),
        isUser: false,
      };
      setMessages(prevMessages => [response, ...prevMessages]);
    }, 1000);
  };

  return (
    <View style={styles.container}>
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
        onSendText={(text) => addMessage('text', text)}
        onSendImage={(uri) => addMessage('image', uri)}
        onSendAudio={(uri) => addMessage('audio', uri)}
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
}); 