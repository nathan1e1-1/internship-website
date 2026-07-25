import { Internship } from '@/lib/types';

interface FeaturedSectionProps {
  internships: Internship[];
}

function getDeadlineBadge(deadline?: string): { text: string; color: string; darkColor: string } {
  if (!deadline) return { text: 'No deadline', color: 'bg-slate-100 text-slate-600', darkColor: 'dark:bg-slate-800 dark:text-slate-300' };
  const days = Math.ceil((new Date(deadline).getTime() - Date.now()) / (1000 * 60 * 60 * 24));
  if (days < 0) return { text: 'Closed', color: 'bg-slate-100 text-slate-500', darkColor: 'dark:bg-slate-800 dark:text-slate-400' };
  if (days < 14) return { text: `${days}d left`, color: 'bg-red-100 text-red-700', darkColor: 'dark:bg-red-950 dark:text-red-300' };
  if (days < 30) return { text: `${days}d left`, color: 'bg-amber-100 text-amber-700', darkColor: 'dark:bg-amber-950 dark:text-amber-300' };
  return { text: `${days}d left`, color: 'bg-emerald-100 text-emerald-700', darkColor: 'dark:bg-emerald-950 dark:text-emerald-300' };
}

export function FeaturedSection({ internships }: FeaturedSectionProps) {
  if (internships.length === 0) return null;

  return (
    <section className="py-6">
      <h2 className="text-xl font-semibold mb-4 text-foreground">Featured Programs</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {internships.map((internship) => {
          const badge = getDeadlineBadge(internship.deadline);
          return (
            <div
              key={internship.id}
              className="border border-border rounded-xl p-5 bg-card hover:shadow-lg hover:border-primary/30 transition-all duration-200"
            >
              <div className="flex justify-between items-start mb-3">
                <h3 className="font-bold text-lg text-card-foreground">{internship.company}</h3>
                <div className="flex gap-2">
                  {internship.season && (
                    <span className="text-xs px-2.5 py-1 rounded-full font-medium bg-blue-100 text-blue-700 dark:bg-blue-950 dark:text-blue-300">
                      {internship.season}
                    </span>
                  )}
                  <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${badge.color} ${badge.darkColor}`}>
                    {badge.text}
                  </span>
                </div>
              </div>
              <p className="text-muted-foreground mb-4 text-sm">{internship.title}</p>
              <a
                href={internship.url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-secondary transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 focus:ring-offset-background"
              >
                Apply
                <svg className="ml-1.5 w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </a>
            </div>
          );
        })}
      </div>
    </section>
  );
}
