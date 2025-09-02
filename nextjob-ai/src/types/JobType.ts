export type JobOffer = {
   id: number;
  user_id?: number | null;
  email?: string | null;
  match_score: number;
  reason?: string | null;
  technologies_matched?: string | null;
  title?: string | null;
  company?: string | null;
  location?: string | null;
  description?: string | null;
  apply_link?: string | null;
  created_at: string; // ISO
};
