export interface Offer {
  id: string;
  title: string;
  description: string;
  price: number;
  images: string[];
  seller: {
    id: string;
    name: string;
  };
  createdAt: string;
  condition: 'new' | 'used' | 'good' | 'fair';
  location: string;
}

export interface OfferFilters {
  search: string;
  minPrice?: number;
  maxPrice?: number;
  condition?: string;
  sortBy: 'price' | 'date' | 'popularity';
}