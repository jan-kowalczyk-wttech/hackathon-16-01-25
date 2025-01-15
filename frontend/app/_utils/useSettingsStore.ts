import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface SettingsState {
  username: string;
  setUsername: (username: string) => void;
}

export const useSettingsStore = create<SettingsState>((set) => ({
  username: '',
  setUsername: async (username: string) => {
    await AsyncStorage.setItem('username', username);
    set({ username });
  },
}));

// Load initial username
AsyncStorage.getItem('username').then((username) => {
  if (username) {
    useSettingsStore.getState().setUsername(username);
  }
});

export default useSettingsStore; 