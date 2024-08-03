import type { Category } from "./categories";
import type { User } from "./users";

export interface RecipeItem {
  name: string;
  slug: string;
  thumbnail_image_url: string | null;
  num_ratings: number;
  avg_rating?: number;
  categories: Category[];
}

export interface NutritionInformation {
  calories: number;
  serving_size: number;
  carbohydrate?: number;
  protein?: number;
  fat?: number;
  saturated_fat?: number;
  trans_fat?: number;
  unsaturated_fat?: number;
  cholesterol?: number;
  sodium?: number;
  fiber?: number;
  sugar?: number;
}

export interface Ingredient {
  id: number;
  amount_display?: string;
  food_display: string;
  optional: boolean;
  qualifier: string;
  note: string;
}

export interface Source {
  name: string;
  type: 1 | 2 | 3 | 4;
  value?: string;
}

export interface Recipe extends RecipeItem {
  description: string;
  servings?: number;
  yield_unit?: string;
  yield_amount?: number;
  cook_time?: string;
  prep_time?: string;
  total_time?: string;
  source?: Source;
  source_value?: string;
  nutrition?: NutritionInformation;
  steps: string[];
  added_by: User;
}
