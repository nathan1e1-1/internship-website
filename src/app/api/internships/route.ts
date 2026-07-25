import { NextResponse } from 'next/server';
import { loadInternships } from '@/lib/data';

export async function GET() {
  try {
    const internships = await loadInternships();
    return NextResponse.json(internships);
  } catch (error) {
    console.error('Failed to load internships:', error);
    return NextResponse.json([], { status: 500 });
  }
}
