import { Internship } from '@/lib/types';
import { InternshipCard } from './InternshipCard';

interface InternshipListProps {
  internships: Internship[];
}

export function InternshipList({ internships }: InternshipListProps) {
  if (internships.length === 0) {
    return (
      <div className="py-12 text-center">
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-muted mb-4">
          <svg className="w-6 h-6 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p className="text-muted-foreground font-medium">No internships found right now</p>
        <p className="text-sm text-muted-foreground/70 mt-1">Check back tomorrow for new opportunities</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {internships.map((internship) => (
        <InternshipCard key={internship.id} internship={internship} />
      ))}
    </div>
  );
}
