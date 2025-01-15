import { useEffect, useState } from 'react';
import { StyleSheet, View, Text, ScrollView } from 'react-native';
import { SettingsInput } from '../../(components)/common/SettingsInput';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function SettingsScreen() {
  const [username, setUsername] = useState('');
  const [savedUsername, setSavedUsername] = useState('');

  useEffect(() => {
    // Load saved username when component mounts
    loadUsername();
  }, []);

  useEffect(() => {
    // Save username when it changes (with debounce)
    const timeoutId = setTimeout(() => {
      if (username !== savedUsername) {
        saveUsername(username);
      }
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [username]);

  const loadUsername = async () => {
    try {
      const saved = await AsyncStorage.getItem('username');
      if (saved) {
        setUsername(saved);
        setSavedUsername(saved);
      }
    } catch (error) {
      console.error('Error loading username:', error);
    }
  };

  const saveUsername = async (newUsername: string) => {
    try {
      await AsyncStorage.setItem('username', newUsername);
      setSavedUsername(newUsername);
    } catch (error) {
      console.error('Error saving username:', error);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Profile Settings</Text>
        <SettingsInput
          label="Username"
          value={username}
          onChangeText={setUsername}
          placeholder="Enter your username"
        />
        {username !== savedUsername && (
          <Text style={styles.savingText}>Saving...</Text>
        )}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>App Information</Text>
        <View style={styles.infoItem}>
          <Text style={styles.infoLabel}>Version</Text>
          <Text style={styles.infoValue}>1.0.0</Text>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  section: {
    marginTop: 24,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
    marginBottom: 8,
    marginLeft: 16,
    textTransform: 'uppercase',
  },
  infoItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 16,
    backgroundColor: 'white',
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: '#ccc',
  },
  infoLabel: {
    fontSize: 16,
    color: '#333',
  },
  infoValue: {
    fontSize: 16,
    color: '#666',
  },
  savingText: {
    fontSize: 12,
    color: '#666',
    fontStyle: 'italic',
    marginLeft: 16,
    marginTop: 4,
  },
}); 