export interface BaseCategory {
  name: string;
  name_plural: string | null;
  slug: string;
  thumbnail_image_url: string;
}
export type CategoryType = BaseCategory;

export interface Category extends BaseCategory {
  type: CategoryType;
}
