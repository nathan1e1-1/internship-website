/**
 * Parse location string into display format:
 * - US cities: "San Francisco, CA" → "San Francisco"
 * - International: "Toronto, ON, Canada" → "Canada"
 * - Remote: "Remote in US" → "Remote (US)"
 * - Edge cases: handled gracefully
 */
export function parseLocation(location: string): string {
  if (!location) return 'Unknown';
  
  const trimmed = location.trim();
  
  // Handle remote cases
  if (trimmed.toLowerCase().startsWith('remote')) {
    const lower = trimmed.toLowerCase();
    if (lower.includes('canada')) return 'Remote (Canada)';
    if (lower.includes('us') || lower.includes('usa') || lower.includes('united states')) return 'Remote (US)';
    return 'Remote';
  }
  
  // Check for international countries
  const countries = ['Canada', 'UK', 'Germany', 'France'];
  for (const country of countries) {
    if (trimmed.includes(country)) {
      return country;
    }
  }
  
  // US city pattern: "City, ST" or "City, State"
  // Match pattern like "San Francisco, CA" or "New York, NY"
  const usCityMatch = trimmed.match(/^([^,]+),\s*(?:[A-Z]{2}|[A-Za-z\s]+)$/);
  if (usCityMatch) {
    return usCityMatch[1].trim();
  }
  
  // Edge cases
  if (trimmed === 'California') return 'California';
  if (trimmed === 'United States') return 'United States';
  if (trimmed === 'NYC' || trimmed === 'SF' || trimmed === 'LA') return trimmed;
  
  // If it has commas but no country match, might be multi-location
  if (trimmed.includes(',')) {
    // Try to extract first city
    const firstPart = trimmed.split(',')[0].trim();
    if (firstPart) return firstPart;
  }
  
  return trimmed;
}

/**
 * Get all unique parsed locations from a list of internships
 */
export function getUniqueLocations(locations: string[]): string[] {
  const parsed = locations.map(parseLocation);
  return Array.from(new Set(parsed)).sort();
}
