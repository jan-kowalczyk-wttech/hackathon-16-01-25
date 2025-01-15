import { Offer } from '../../(types)/offer.types';

export const mockOffers: Offer[] = [
  {
    id: '1',
    title: 'iPhone 13 Pro',
    description: 'Excellent condition, barely used. Comes with original box and accessories.',
    price: 699.99,
    images: [
      'https://picsum.photos/400/400',
      'https://picsum.photos/400/401',
      'https://picsum.photos/400/402',
    ],
    seller: {
      id: 'seller1',
      name: 'John Doe',
    },
    createdAt: new Date().toISOString(),
    condition: 'good',
    location: 'New York, NY',
  },
  {
    id: '2',
    title: 'MacBook Pro M1',
    description: 'Brand new, sealed in box. 13-inch, 8GB RAM, 256GB SSD.',
    price: 1099.99,
    images: [
      'https://picsum.photos/400/403',
      'https://picsum.photos/400/404',
    ],
    seller: {
      id: 'seller2',
      name: 'Jane Smith',
    },
    createdAt: new Date().toISOString(),
    condition: 'new',
    location: 'Los Angeles, CA',
  },
];

export default mockOffers; 