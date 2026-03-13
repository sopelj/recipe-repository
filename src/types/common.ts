export interface GridItem {
  name: string;
  name_plural?: string | null;
  slug: string;
  thumbnail_url: string | null;
}

export interface OrderableItem {
  id: number | null;
  order: number;
  deleted?: boolean;
}

export type OrderableItems = OrderableItem[];
