import type { Category } from "./categories.ts";

export interface RecipeItem {
    name: string;
    slug: string;
    thumbnail_url: string | null;
    num_ratings: number;
    avg_rating: number | null;
    categories: Category[];
}

export interface Recipe extends RecipeItem {}
