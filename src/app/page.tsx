'use client';

import { useState, useEffect, useMemo } from 'react';
import { Internship } from '@/lib/types';
import { Header } from '@/components/Header';
import { FeaturedSection } from '@/components/FeaturedSection';
import { FilterBar } from '@/components/FilterBar';
import { InternshipList } from '@/components/InternshipList';
import { Footer } from '@/components/Footer';

interface Filters {
  company: string;
  type: string;
  workType: string;
  season: string;
}

export default function Home() {
  const [internships, setInternships] = useState<Internship[]>([]);
  const [activeFilters, setActiveFilters] = useState<Filters>({ company: '', type: '', workType: '', season: '' });
  const [lastUpdated, setLastUpdated] = useState<string>('unknown');
  const [isLoading, setIsLoading] = useState(true);
  const [compactView, setCompactView] = useState(true);

  useEffect(() => {
    fetch('/api/internships')
      .then((res) => res.json())
      .then((data: Internship[]) => {
        const sorted = [...data].sort((a, b) => {
          const dateA = a.date_posted || '';
          const dateB = b.date_posted || '';
          return dateB.localeCompare(dateA);
        });
        setInternships(sorted);
        if (sorted.length > 0) {
          setLastUpdated(sorted[0].date_scraped);
        }
      })
      .catch((err) => {
        console.error('Failed to fetch internships:', err);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, []);

  const filtered = useMemo(() => {
    let result = internships;
    if (activeFilters.company) {
      result = result.filter((i) => i.company === activeFilters.company);
    }
    if (activeFilters.type) {
      result = result.filter((i) => i.type === activeFilters.type);
    }
    if (activeFilters.workType) {
      result = result.filter((i) => i.work_type === activeFilters.workType);
    }
    if (activeFilters.season) {
      result = result.filter((i) => i.season === activeFilters.season);
    }
    return result;
  }, [internships, activeFilters]);

  const featured = useMemo(() => filtered.filter((i) => i.category === 'top-tier'), [filtered]);
  const general = useMemo(() => filtered.filter((i) => i.category === 'general'), [filtered]);

  const filters = useMemo(() => ({
    companies: Array.from(new Set(internships.map((i) => i.company))).sort(),
    types: Array.from(new Set(internships.map((i) => i.type))).sort(),
    workTypes: Array.from(new Set(internships.map((i) => i.work_type))).sort(),
    seasons: Array.from(new Set(internships.map((i) => i.season).filter((s): s is string => !!s))).sort(),
  }), [internships]);

  return (
    <main className="min-h-screen bg-background text-foreground transition-colors duration-200">
      <div className="max-w-5xl mx-auto px-4">
        <Header lastUpdated={lastUpdated} />

        {isLoading ? (
          <div className="py-16 text-center">
            <div className="inline-block w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin mb-4" />
            <p className="text-muted-foreground">Loading opportunities...</p>
          </div>
        ) : (
          <>
            <FeaturedSection internships={featured} />
            <section className="py-6">
              <div className="flex items-center justify-between mb-2">
                <h2 className="text-xl font-semibold text-foreground">All Opportunities</h2>
                <span className="text-sm text-muted-foreground">{general.length} found</span>
              </div>
              <FilterBar
                filters={filters}
                activeFilters={activeFilters}
                onChange={setActiveFilters}
                onClear={() => setActiveFilters({ company: '', type: '', workType: '', season: '' })}
                compact={compactView}
                onToggleCompact={() => setCompactView(!compactView)}
              />
              <InternshipList internships={general} compact={compactView} />
            </section>
          </>
        )}

        <Footer />
      </div>
    </main>
  );
}
