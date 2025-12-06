import { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { Stats, Ranking } from '../types/index';
import KPICard from './KPICard';
import CategoryCard from './CategoryCard';
import RankingTable from './RankingTable';
import { getCategoryBadge } from '../utils/formatters';
import styles from '../css/Dashboard.module.css';

function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [ranking, setRanking] = useState<Ranking | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [statsData, rankingData] = await Promise.all([
          api.getStats(),
          api.getRanking(undefined, 10),
        ]);
        setStats(statsData);
        setRanking(rankingData);
        setError(null);
      } catch (err) {
        setError('Błąd połączenia z API. Czy backend działa?');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className={styles.dashboard}>
        <div className={styles.loading}>Ładowanie danych...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.dashboard}>
        <div className={styles.error}>{error}</div>
      </div>
    );
  }

  if (!stats || !ranking) {
    return null;
  }

  return (
    <div className={styles.dashboard}>
      <header className={styles.dashboardHeader}>
        <div className={styles.pkoLogo}><img src="https://upload.wikimedia.org/wikipedia/commons/5/56/Logotyp_PKO_BP.jpg" /></div>
        <h1>Indeks Branż Polski</h1>
      </header>

      <div className={styles.kpiGrid}>
        <KPICard label="Analizowane branże" value={stats.total_industries} />
        <KPICard
          label="Top branża"
          value={stats.top_industry.score.toFixed(1)}
          subtitle={stats.top_industry.name}
          variant="success"
        />
        <KPICard
          label="Najsłabsza branża"
          value={stats.worst_industry.score.toFixed(1)}
          subtitle={stats.worst_industry.name}
          variant="danger"
        />
        <KPICard label="Ostatnia aktualizacja" value={stats.last_update} />
      </div>

      <div className={styles.section}>
        <h2>Rozkład kategorii</h2>
        <div className={styles.categoryGrid}>
          {Object.entries(stats.categories).map(([cat, count]) => {
            const badge = getCategoryBadge(cat);
            return (
              <CategoryCard
                key={cat}
                category={cat}
                label={badge.label}
                count={count}
                color={badge.color}
              />
            );
          })}
        </div>
      </div>

      <div className={styles.rankingsGrid}>
        <RankingTable
          title="TOP 10 - Najlepsze branże"
          industries={ranking.top}
          variant="success"
        />
        <RankingTable
          title="BOTTOM 10 - Wymagające uwagi"
          industries={ranking.bottom}
          variant="danger"
        />
      </div>
    </div>
  );
}

export default Dashboard;
