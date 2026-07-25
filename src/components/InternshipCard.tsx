import { Internship } from '@/lib/types';
import { formatRelativeDate, isNew } from '@/lib/dates';

interface InternshipCardProps {
  internship: Internship;
  compact?: boolean;
}

export function InternshipCard({ internship, compact = true }: InternshipCardProps) {
  const isNewListing = isNew(internship.date_posted, 7);
  const relativeDate = formatRelativeDate(internship.date_posted);

  return (
    <div 
      className="border border-border rounded-lg px-4 py-3 bg-card hover:shadow-md hover:-translate-y-0.5 hover:border-primary/40 transition-all duration-200 ease-out group"
    >
      <div className="flex items-center justify-between gap-3">
        {/* Main info - left side */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="font-semibold text-sm text-card-foreground truncate group-hover:text-primary transition-colors duration-200">
              {internship.title}
            </h3>
            <span className="text-xs text-muted-foreground shrink-0">
              @ {internship.company}
            </span>
            {isNewListing && (
              <span className="text-xs px-1.5 py-0.5 rounded-full bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300 shrink-0 font-medium">
                New
              </span>
            )}
            {internship.notes && (
              <span className="text-xs px-1.5 py-0.5 rounded bg-amber-100 text-amber-700 dark:bg-amber-950 dark:text-amber-300 shrink-0" title={internship.notes}>
                {internship.notes.length > 30 ? internship.notes.slice(0, 30) + '...' : internship.notes}
              </span>
            )}
          </div>
          <div className="flex items-center gap-3 mt-1 text-xs text-muted-foreground flex-wrap">
            <span className="flex items-center gap-1">
              <svg className="w-3 h-3 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              {internship.location}
            </span>
            <span className="flex items-center gap-1" title={internship.date_posted || 'Unknown'}>
              <svg className="w-3 h-3 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {relativeDate}
            </span>
            <span className="px-1.5 py-0.5 rounded-full bg-muted text-muted-foreground font-medium">
              {internship.work_type}
            </span>
            {internship.season && (
              <span className="px-1.5 py-0.5 rounded-full bg-blue-100 text-blue-700 dark:bg-blue-950 dark:text-blue-300 font-medium">
                {internship.season}
              </span>
            )}
          </div>
        </div>

        {/* Apply button - right side */}
        <a
          href={internship.url}
          target="_blank"
          rel="noopener noreferrer"
          className="shrink-0 inline-flex items-center px-3 py-1.5 bg-primary text-primary-foreground rounded-md text-xs font-medium hover:bg-secondary transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-1 focus:ring-offset-background group-hover:scale-105"
        >
          Apply
          <svg className="ml-1 w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
        </a>
      </div>
    </div>
  );
}
