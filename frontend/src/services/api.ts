import type { Stats, Ranking, IndustriesResponse } from '../types/index';
import { API_BASE_URL } from '../constants';

export const api = {
  async getStats(): Promise<Stats> {
    const response = await fetch(`${API_BASE_URL}/api/stats`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
  },

  async getRanking(year?: number, top: number = 10): Promise<Ranking> {
    const params = new URLSearchParams();
    if (year) params.append('year', year.toString());
    params.append('top', top.toString());

    const response = await fetch(`${API_BASE_URL}/api/ranking?${params}`);
    if (!response.ok) throw new Error('Failed to fetch ranking');
    return response.json();
  },

  async getIndustries(year?: number, category?: string, limit?: number): Promise<IndustriesResponse> {
    const params = new URLSearchParams();
    if (year) params.append('year', year.toString());
    if (category) params.append('category', category);
    if (limit) params.append('limit', limit.toString());

    const response = await fetch(`${API_BASE_URL}/api/industries?${params}`);
    if (!response.ok) throw new Error('Failed to fetch industries');
    return response.json();
  },

  async getIndustryDetails(pkdCode: string): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/api/industries/${pkdCode}`);
    if (!response.ok) throw new Error('Failed to fetch industry details');
    return response.json();
  },
};
