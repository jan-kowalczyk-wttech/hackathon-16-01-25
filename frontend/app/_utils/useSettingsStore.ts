import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface SettingsState {
  username: string;
  setUsername: (username: string) => void;
}

// Generate a random username like "User1234"
const generateRandomUsername = () => {
  const randomNum = Math.floor(1000 + Math.random() * 9000);
  return `User${randomNum}`;
};

export const useSettingsStore = create<SettingsState>((set) => ({
  username: '',
  setUsername: async (username: string) => {
    await AsyncStorage.setItem('username', username);
    set({ username });
  },
}));

// Load initial username or create a random one
AsyncStorage.getItem('username').then((username) => {
  if (username) {
    useSettingsStore.getState().setUsername(username);
  } else {
    // If no username is set, generate and save a random one
    const randomUsername = generateRandomUsername();
    useSettingsStore.getState().setUsername(randomUsername);
  }
});

export default useSettingsStore; 