import { StyleSheet, View, Text, Image, TouchableOpacity, AccessibilityInfo } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { Audio } from 'expo-av';
import { colors } from '../../theme/colors';

interface MessageBubbleProps {
  type: 'text' | 'image' | 'audio';
  content: string;
  timestamp: string;
  isUser?: boolean;
}

export function MessageBubble({ type, content, timestamp, isUser }: MessageBubbleProps) {
  const playAudio = async () => {
    if (type !== 'audio') return;

    const sound = new Audio.Sound();
    try {
      await sound.loadAsync({ uri: content });
      await sound.playAsync();
    } catch (error) {
      console.error('Error playing audio:', error);
    }
  };

  return (
    <View 
      style={[styles.container, isUser ? styles.userContainer : styles.otherContainer]}
      accessible={true}
      accessibilityLabel={`${isUser ? 'Your' : 'Their'} ${type} message: ${content}`}
      accessibilityHint={type === 'audio' ? 'Double tap to play audio' : undefined}
    >
      {type === 'text' && (
        <Text style={[
          styles.text,
          isUser ? styles.userText : styles.otherText
        ]}>
          {content}
        </Text>
      )}

      {type === 'image' && (
        <Image 
          source={{ uri: content }} 
          style={styles.image}
          accessible={true}
          accessibilityLabel="Message image"
        />
      )}

      {type === 'audio' && (
        <TouchableOpacity 
          style={[styles.audioButton, isUser ? styles.userAudioButton : styles.otherAudioButton]} 
          onPress={playAudio}
        >
          <MaterialIcons 
            name="play-arrow" 
            size={24} 
            color={isUser ? colors.text.onPrimary : colors.primary} 
          />
          <Text style={[
            styles.audioText,
            isUser ? styles.userAudioText : styles.otherAudioText
          ]}>
            Play Audio
          </Text>
        </TouchableOpacity>
      )}

      <Text style={[
        styles.timestamp,
        isUser ? styles.userTimestamp : styles.otherTimestamp
      ]}>
        {timestamp}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    maxWidth: '80%',
    marginVertical: 4,
    marginHorizontal: 8,
    padding: 12,
    borderRadius: 20,
    elevation: 1,
    shadowColor: colors.gray[900],
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  userContainer: {
    alignSelf: 'flex-end',
    backgroundColor: colors.primary,
    borderBottomRightRadius: 4,
  },
  otherContainer: {
    alignSelf: 'flex-start',
    backgroundColor: colors.gray[100],
    borderBottomLeftRadius: 4,
  },
  text: {
    fontSize: 16,
    lineHeight: 22,
  },
  userText: {
    color: colors.text.onPrimary,
  },
  otherText: {
    color: colors.text.primary,
  },
  image: {
    width: 200,
    height: 200,
    borderRadius: 12,
  },
  audioButton: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 8,
    borderRadius: 16,
  },
  userAudioButton: {
    backgroundColor: colors.primaryDark,
  },
  otherAudioButton: {
    backgroundColor: colors.gray[200],
  },
  audioText: {
    marginLeft: 8,
    fontSize: 16,
  },
  userAudioText: {
    color: colors.text.onPrimary,
  },
  otherAudioText: {
    color: colors.primary,
  },
  timestamp: {
    fontSize: 12,
    marginTop: 4,
    alignSelf: 'flex-end',
  },
  userTimestamp: {
    color: colors.text.onPrimary,
    opacity: 0.8,
  },
  otherTimestamp: {
    color: colors.text.secondary,
  },
}); 