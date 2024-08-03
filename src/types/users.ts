export interface User {
    id: number;
    first_name: string;
    last_name: string;
    full_name: string;
    initials: string;
    profile_image_url: string | null;
    is_staff: boolean;
}
