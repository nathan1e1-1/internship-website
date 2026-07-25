export interface Internship {
  id: string;
  title: string;
  company: string;
  type: 'internship' | 'fellowship' | 'program';
  category: 'top-tier' | 'general';
  url: string;
  location: string;
  work_type: 'remote' | 'hybrid' | 'in-person';
  eligibility?: string;
  date_posted?: string;
  deadline?: string;
  notes?: string;
  date_scraped: string;
}
