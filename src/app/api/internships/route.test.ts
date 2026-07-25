/**
 * @jest-environment node
 */
import { GET } from './route';

describe('/api/internships', () => {
  it('returns JSON array of internships', async () => {
    const response = await GET();
    expect(response.status).toBe(200);
    const body = await response.json();
    expect(Array.isArray(body)).toBe(true);
    expect(body.length).toBeGreaterThan(0);
    expect(body[0]).toHaveProperty('id');
    expect(body[0]).toHaveProperty('company');
  });
});
