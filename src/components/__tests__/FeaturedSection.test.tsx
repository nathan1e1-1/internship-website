import { render, screen } from '@testing-library/react';
import { FeaturedSection } from '../FeaturedSection';
import { Internship } from '@/lib/types';

const mockFeatured: Internship[] = [
  {
    id: 'nvidia-ignite-2026',
    title: 'NVIDIA Ignite',
    company: 'NVIDIA',
    type: 'internship',
    category: 'top-tier',
    url: 'https://nvidia.com',
    location: 'Santa Clara, CA',
    work_type: 'hybrid',
    deadline: '2025-10-01',
    date_scraped: '2025-07-24',
  },
];

describe('FeaturedSection', () => {
  it('renders featured cards', () => {
    render(<FeaturedSection internships={mockFeatured} />);
    expect(screen.getByText('NVIDIA Ignite')).toBeInTheDocument();
    expect(screen.getByText('NVIDIA')).toBeInTheDocument();
    expect(screen.getByText('Apply')).toHaveAttribute('href', 'https://nvidia.com');
  });
});
