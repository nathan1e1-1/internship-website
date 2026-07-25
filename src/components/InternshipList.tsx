import { Internship } from '@/lib/types';
import { InternshipCard } from './InternshipCard';

interface InternshipListProps {
  internships: Internship[];
}

export function InternshipList({ internships }: InternshipListProps) {
  if (internships.length === 0) {
    return (
      <div className="py-8 text-center text-gray-500">
        <p>No internships found right now. Check back tomorrow!</p>
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
