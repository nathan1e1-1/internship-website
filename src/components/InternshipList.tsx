import { Internship } from '@/lib/types';
import { InternshipCard } from './InternshipCard';

interface InternshipListProps {
  internships: Internship[];
  compact?: boolean;
}

export function InternshipList({ internships, compact = true }: InternshipListProps) {
  if (internships.length === 0) {
    return (
      <div className="py-16 text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-muted mb-5">
          <svg className="w-8 h-8 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <h3 className="text-lg font-semibold text-foreground mb-1">No matches found</h3>
        <p className="text-sm text-muted-foreground max-w-sm mx-auto">
          Try adjusting your filters or clearing them to see more opportunities. New internships are added daily!
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {internships.map((internship) => (
        <InternshipCard key={internship.id} internship={internship} compact={compact} />
      ))}
    </div>
  );
}
