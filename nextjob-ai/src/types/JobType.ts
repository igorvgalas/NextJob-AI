export type JobType = {
  id: number;
  match_score: number;
  reason: string;
  technologies_matched: string[];
  title: string;
  company: string;
  location: string;
  description: string;
  apply_link: string;
  created_at: string;
};
