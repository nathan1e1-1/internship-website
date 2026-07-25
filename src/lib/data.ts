import { Internship } from './types';

export async function loadInternships(): Promise<Internship[]> {
  const fs = await import('fs/promises');
  const path = await import('path');
  const filePath = path.join(process.cwd(), 'data', 'internships.json');
  const raw = await fs.readFile(filePath, 'utf-8');
  const data = JSON.parse(raw);
  if (!Array.isArray(data)) {
    throw new Error(' internships.json must be an array');
  }
  return data as Internship[];
}
