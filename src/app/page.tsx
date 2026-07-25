'use client';

import { useState, useEffect } from 'react';
import { Internship } from '@/lib/types';
import { Header } from '@/components/Header';
import { FeaturedSection } from '@/components/FeaturedSection';
import { FilterBar } from '@/components/FilterBar';
import { InternshipList } from '@/components/InternshipList';
import { Footer } from '@/components/Footer';

interface Filters {
  company: string;
  location: string;
  type: string;
  workType: string;
}

export default function Home() {
  const [internships, setInternships] = useState<Internship[]>([]);
  const [filtered, setFiltered] = useState<Internship[]>([]);
  const [activeFilters, setActiveFilters] = useState<Filters>({ company: '', location: '', type: '', workType: '' });
  const [lastUpdated, setLastUpdated] = useState<string>('unknown');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch('/api/internships')
      .then((res) => res.json())
      .then((data: Internship[]) => {
        setInternships(data);
        setFiltered(data);
        if (data.length > 0) {
          setLastUpdated(data[0].date_scraped);
        }
      })
      .catch((err) => {
        console.error('Failed to fetch internships:', err);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, []);

  useEffect(() => {
    let result = [...internships];
    if (activeFilters.company) result = result.filter((i) => i.company === activeFilters.company);
    if (activeFilters.location) result = result.filter((i) => i.location === activeFilters.location);
    if (activeFilters.type) result = result.filter((i) => i.type === activeFilters.type);
    if (activeFilters.workType) result = result.filter((i) => i.work_type === activeFilters.workType);
    setFiltered(result);
  }, [activeFilters, internships]);

  const featured = filtered.filter((i) => i.category === 'top-tier');
  const general = filtered.filter((i) => i.category === 'general');

  const filters = {
    companies: Array.from(new Set(internships.map((i) => i.company))).sort(),
    locations: Array.from(new Set(internships.map((i) => i.location))).sort(),
    types: Array.from(new Set(internships.map((i) => i.type))).sort(),
    workTypes: Array.from(new Set(internships.map((i) => i.work_type))).sort(),
  };

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
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold text-foreground">All Opportunities</h2>
                <span className="text-sm text-muted-foreground">{general.length} found</span>
              </div>
              <FilterBar
                filters={filters}
                activeFilters={activeFilters}
                onChange={setActiveFilters}
                onClear={() => setActiveFilters({ company: '', location: '', type: '', workType: '' })}
              />
              <InternshipList internships={general} />
            </section>
          </>
        )}

        <Footer />
      </div>
    </main>
  );
}
