export interface User {
    email: string;
    username: string;
    first_name: string;
    last_name: string;
    profile_image_url: string | null;
}

export interface Category {
    name: string;
    name_plural: string | null;
    slug: string;
    thumbnail_image_url: string;
}
