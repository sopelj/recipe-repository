import type { Category } from "./categories";
import type { User } from "./users";

export interface BaseRecipe {
  name: string;
  slug: string;
}

export interface RecipeItem extends BaseRecipe {
  thumbnail_url: string | null;
  num_ratings: number;
  avg_rating: number | null;
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
  group_id: number | null;
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

export interface IngredientGroup {
  id: number;
  name: string;
}

export interface YieldUnit {
  name: string;
  name_plural?: string;
}

export interface Recipe extends Omit<RecipeItem, "thumbnail_url"> {
  description: string;
  image_url: string | null;
  servings?: number;
  yield_unit?: YieldUnit;
  yield_amount?: number;
  cook_time?: string;
  prep_time?: string;
  total_time?: string;
  source?: Source;
  ingredient_groups: IngredientGroup[];
  parent_recipes?: BaseRecipe[];
  source_value?: string;
  nutrition?: NutritionInformation;
  steps: string[];
  added_by: User;
}
