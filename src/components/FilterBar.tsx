interface FilterOptions {
  companies: string[];
  locations: string[];
  types: string[];
  workTypes: string[];
}

interface ActiveFilters {
  company: string;
  location: string;
  type: string;
  workType: string;
}

interface FilterBarProps {
  filters: FilterOptions;
  activeFilters?: ActiveFilters;
  onChange: (filters: ActiveFilters) => void;
  onClear: () => void;
}

export function FilterBar({ filters, activeFilters, onChange, onClear }: FilterBarProps) {
  const current = activeFilters || { company: '', location: '', type: '', workType: '' };

  const handleChange = (field: keyof ActiveFilters, value: string) => {
    onChange({ ...current, [field]: value });
  };

  return (
    <div className="flex flex-wrap gap-3 py-4 items-center">
      <div>
        <label htmlFor="company" className="sr-only">Company</label>
        <select
          id="company"
          value={current.company}
          onChange={(e) => handleChange('company', e.target.value)}
          className="border border-border rounded-lg px-3 py-2 text-sm bg-card text-card-foreground focus:outline-none focus:ring-2 focus:ring-ring"
        >
          <option value="">All Companies</option>
          {filters.companies.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>
      <div>
        <label htmlFor="location" className="sr-only">Location</label>
        <select
          id="location"
          value={current.location}
          onChange={(e) => handleChange('location', e.target.value)}
          className="border border-border rounded-lg px-3 py-2 text-sm bg-card text-card-foreground focus:outline-none focus:ring-2 focus:ring-ring"
        >
          <option value="">All Locations</option>
          {filters.locations.map((l) => (
            <option key={l} value={l}>{l}</option>
          ))}
        </select>
      </div>
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
      <button
        onClick={onClear}
        className="text-sm text-primary hover:text-secondary font-medium transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-ring rounded px-2 py-1"
      >
        Clear all
      </button>
    </div>
  );
}
