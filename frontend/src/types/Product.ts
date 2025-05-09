export interface Product {
  id: number;
  name: string;
  price: number;
  description?: string;
  brand?: string;
  quantity: number;
  category?: {
    id: string;
    title: string;
    description: string;
  };
}

export interface Category {
  id: string;
  title: string;
  description: string;
}