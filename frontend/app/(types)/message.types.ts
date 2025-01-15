export interface Message {
  id: string;
  type: 'text' | 'image' | 'audio';
  content: string;
  timestamp: string;
  sender: {
    id: string;
    name: string;
  };
}