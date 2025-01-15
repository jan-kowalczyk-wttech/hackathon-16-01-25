import { Offer } from '../../(types)/offer.types';
import { mockOffers } from '../mock/mockOffers';

const API_URL = 'https://your-api-url.com';

export async function fetchOffers(): Promise<Offer[]> {
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // In real app, you would use:
    // const response = await fetch(`${API_URL}/offers`);
    // const data = await response.json();
    // return data;
    
    return mockOffers;
  } catch (error) {
    console.error('Error fetching offers:', error);
    return mockOffers; // Fallback to mock data
  }
}

export default { fetchOffers }; 