import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Home from './page';

// Mock the fetch API
const mockInternships = [
  {
    id: 'appian-1',
    title: 'Software Engineer Intern',
    company: 'Appian',
    type: 'internship',
    category: 'general',
    url: 'https://appian.com',
    location: 'McLean, VA',
    work_type: 'in-person',
    date_posted: '2025-07-24',
    date_scraped: '2025-07-25',
  },
  {
    id: 'tenstorrent-1',
    title: 'SWE Intern - Power Modeling',
    company: 'Tenstorrent',
    type: 'internship',
    category: 'general',
    url: 'https://tenstorrent.com',
    location: 'Santa Clara, CA',
    work_type: 'in-person',
    date_posted: '2025-07-23',
    date_scraped: '2025-07-25',
  },
  {
    id: 'nvidia-ignite',
    title: 'NVIDIA Ignite',
    company: 'NVIDIA',
    type: 'internship',
    category: 'top-tier',
    url: 'https://nvidia.com',
    location: 'Santa Clara, CA',
    work_type: 'hybrid',
    date_posted: '2025-07-15',
    date_scraped: '2025-07-25',
  },
];

describe('Home Page Filtering', () => {
  beforeEach(() => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockInternships),
      })
    ) as jest.Mock;
  });

  it('shows all internships initially, then filters by company correctly', async () => {
    render(<Home />);

    // Wait for data to load
    await waitFor(() => {
      expect(screen.getByText('Software Engineer Intern')).toBeInTheDocument();
    });

    // Should show 2 general initially (top-tier is in featured section)
    expect(screen.getByText(/2 found/)).toBeInTheDocument();

    // Filter by Appian
    const companySelect = screen.getByLabelText(/company/i);
    fireEvent.change(companySelect, { target: { value: 'Appian' } });

    // Should now show only 1
    await waitFor(() => {
      expect(screen.getByText(/1 found/)).toBeInTheDocument();
    });

    // Should show Appian but NOT Tenstorrent
    expect(screen.getByText('Software Engineer Intern')).toBeInTheDocument();
    expect(screen.queryByText('SWE Intern - Power Modeling')).not.toBeInTheDocument();
  });

  it('changes filter to a different company and updates the list', async () => {
    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText('Software Engineer Intern')).toBeInTheDocument();
    });

    // Filter by Appian
    const companySelect = screen.getByLabelText(/company/i);
    fireEvent.change(companySelect, { target: { value: 'Appian' } });

    await waitFor(() => {
      expect(screen.getByText(/1 found/)).toBeInTheDocument();
    });

    // Now change filter to Tenstorrent
    fireEvent.change(companySelect, { target: { value: 'Tenstorrent' } });

    await waitFor(() => {
      expect(screen.getByText(/1 found/)).toBeInTheDocument();
    });

    // Should show Tenstorrent but NOT Appian
    expect(screen.getByText('SWE Intern - Power Modeling')).toBeInTheDocument();
    expect(screen.queryByText('Software Engineer Intern')).not.toBeInTheDocument();
  });

  it('clears filter and shows all again', async () => {
    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText('Software Engineer Intern')).toBeInTheDocument();
    });

    // Filter by Appian
    const companySelect = screen.getByLabelText(/company/i);
    fireEvent.change(companySelect, { target: { value: 'Appian' } });

    await waitFor(() => {
      expect(screen.getByText(/1 found/)).toBeInTheDocument();
    });

    // Clear filter
    const clearButton = screen.getByText(/clear all/i);
    fireEvent.click(clearButton);

    // Should show 2 general again (top-tier is in featured section)
    await waitFor(() => {
      expect(screen.getByText(/2 found/)).toBeInTheDocument();
    });

    expect(screen.getByText('Software Engineer Intern')).toBeInTheDocument();
    expect(screen.getByText('SWE Intern - Power Modeling')).toBeInTheDocument();
  });
});
