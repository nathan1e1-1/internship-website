interface FilterOptions {
  companies: string[];
  types: string[];
  workTypes: string[];
  seasons: string[];
  locations: string[];
}

interface ActiveFilters {
  company: string;
  type: string;
  workType: string;
  season: string;
  location: string;
}

interface FilterBarProps {
  filters: FilterOptions;
  activeFilters?: ActiveFilters;
  onChange: (filters: ActiveFilters) => void;
  onClear: () => void;
  compact?: boolean;
  onToggleCompact?: () => void;
}

export function FilterBar({ filters, activeFilters, onChange, onClear, compact = true, onToggleCompact }: FilterBarProps) {
  const current = activeFilters || { company: '', type: '', workType: '', season: '', location: '' };

  const handleChange = (field: keyof ActiveFilters, value: string) => {
    onChange({ ...current, [field]: value });
  };

  const hasActiveFilters = current.company || current.type || current.workType || current.season || current.location;

  return (
    <div className="sticky top-0 z-30 bg-background/80 backdrop-blur-md border-b border-border py-3 -mx-4 px-4 mb-4">
      <div className="flex flex-wrap gap-2 items-center">
        {/* Compact text inputs for high-cardinality filters */}
        <div className="relative">
          <label htmlFor="company" className="sr-only">Company</label>
          <div className="relative">
            <input
              id="company"
              list="company-list"
              value={current.company}
              onChange={(e) => handleChange('company', e.target.value)}
              placeholder="Company..."
              className="border border-border rounded-lg pl-3 pr-8 py-2 text-sm bg-card text-card-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring w-36"
            />
            {current.company && (
              <button
                onClick={() => handleChange('company', '')}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                aria-label="Clear company filter"
              >
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
          <datalist id="company-list">
            {filters.companies.map((c) => (
              <option key={c} value={c} />
            ))}
          </datalist>
        </div>

        <div className="relative">
          <label htmlFor="location" className="sr-only">Location</label>
          <div className="relative">
            <input
              id="location"
              list="location-list"
              value={current.location}
              onChange={(e) => handleChange('location', e.target.value)}
              placeholder="Location..."
              className="border border-border rounded-lg pl-3 pr-8 py-2 text-sm bg-card text-card-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring w-32"
            />
            {current.location && (
              <button
                onClick={() => handleChange('location', '')}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                aria-label="Clear location filter"
              >
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
          <datalist id="location-list">
            {filters.locations.map((l) => (
              <option key={l} value={l} />
            ))}
          </datalist>
        </div>

        {/* Dropdowns for low-cardinality filters */}
        <div>
          <label htmlFor="type" className="sr-only">Type</label>
          <select
            id="type"
            value={current.type}
            onChange={(e) => handleChange('type', e.target.value)}
            className="border border-border rounded-lg px-3 py-2 text-sm bg-card text-card-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option value="">All Types</option>
            {filters.types.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="workType" className="sr-only">Work Type</label>
          <select
            id="workType"
            value={current.workType}
            onChange={(e) => handleChange('workType', e.target.value)}
            className="border border-border rounded-lg px-3 py-2 text-sm bg-card text-card-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option value="">All Work Types</option>
            {filters.workTypes.map((w) => (
              <option key={w} value={w}>{w}</option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="season" className="sr-only">Season</label>
          <select
            id="season"
            value={current.season}
            onChange={(e) => handleChange('season', e.target.value)}
            className="border border-border rounded-lg px-3 py-2 text-sm bg-card text-card-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option value="">All Seasons</option>
            {filters.seasons.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>
        
        <div className="flex items-center gap-2 ml-auto">
          {hasActiveFilters && (
            <button
              onClick={onClear}
              className="text-sm text-primary hover:text-secondary font-medium transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-ring rounded px-2 py-1"
            >
              Clear all
            </button>
          )}
          
          {onToggleCompact && (
            <button
              onClick={onToggleCompact}
              className="inline-flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-medium rounded-lg border border-border hover:bg-muted transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-ring"
              title={compact ? "Switch to expanded view" : "Switch to compact view"}
            >
              {compact ? (
                <>
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  </svg>
                  Compact
                </>
              ) : (
                <>
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                  </svg>
                  Expanded
                </>
              )}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
