import { getTrendLabel, getTrendClass } from '../utils/formatters';
import styles from '../css/RankingTable.module.css';

interface Industry {
  pkd_code: string;
  pkd_2007: string;
  pkd_2025: string;
  name: string;
  index_score: number;
  category: string;
  trend: string;
}

interface RankingTableProps {
  title: string;
  industries: Industry[];
  variant: 'success' | 'danger';
}

function RankingTable({ title, industries, variant }: RankingTableProps) {
  return (
    <div className={styles.section}>
      <h2>{title}</h2>
      <div className={styles.rankingTable}>
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>PKD</th>
              <th>Nazwa branży</th>
              <th>Indeks</th>
              <th>Trend</th>
            </tr>
          </thead>
          <tbody>
            {industries.map((industry, index) => (
              <tr key={industry.pkd_code}>
                <td className={styles.rank}>{index + 1}</td>
                <td className={styles.pkdCode}>{industry.pkd_2025}</td>
                <td className={styles.industryName}>{industry.name}</td>
                <td className={styles.score}>
                  <span className={`${styles.scoreBadge} ${styles[variant]}`}>
                    {industry.index_score.toFixed(1)}
                  </span>
                </td>
                <td className={`${styles.trend} ${styles[getTrendClass(industry.trend)]}`}>
                  {getTrendLabel(industry.trend)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default RankingTable;
