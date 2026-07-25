import { Internship } from '@/lib/types';

interface FeaturedSectionProps {
  internships: Internship[];
}

function getDeadlineBadge(deadline?: string): { text: string; color: string } {
  if (!deadline) return { text: 'No deadline', color: 'bg-gray-100 text-gray-600' };
  const days = Math.ceil((new Date(deadline).getTime() - Date.now()) / (1000 * 60 * 60 * 24));
  if (days < 14) return { text: `${days} days left`, color: 'bg-red-100 text-red-700' };
  if (days < 30) return { text: `${days} days left`, color: 'bg-yellow-100 text-yellow-700' };
  return { text: `${days} days left`, color: 'bg-green-100 text-green-700' };
}

export function FeaturedSection({ internships }: FeaturedSectionProps) {
  if (internships.length === 0) return null;

  return (
    <section className="py-6">
      <h2 className="text-xl font-semibold mb-4">Featured Programs</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {internships.map((internship) => {
          const badge = getDeadlineBadge(internship.deadline);
          return (
            <div key={internship.id} className="border rounded-lg p-4 hover:shadow-lg transition-shadow">
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-bold text-lg">{internship.company}</h3>
                <span className={`text-xs px-2 py-1 rounded ${badge.color}`}>
                  {badge.text}
                </span>
              </div>
              <p className="text-gray-700 mb-3">{internship.title}</p>
              <a
                href={internship.url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block px-4 py-2 bg-blue-600 text-white rounded text-sm hover:bg-blue-700"
              >
                Apply
              </a>
            </div>
          );
        })}
      </div>
    </section>
  );
}
