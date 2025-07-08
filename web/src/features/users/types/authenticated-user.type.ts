export type AuthenticatedUser = {
  email: string;
  name: string;
  isEmailVerified: boolean;
  imageUrl: string | null;
};
