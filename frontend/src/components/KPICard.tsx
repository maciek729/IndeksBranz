import styles from '../css/KPICard.module.css';

interface KPICardProps {
  label: string;
  value: string | number;
  subtitle?: string;
  variant?: 'default' | 'success' | 'danger';
}

function KPICard({ label, value, subtitle, variant = 'default' }: KPICardProps) {
  return (
    <div className={`${styles.kpiCard} ${styles[variant]}`}>
      <div className={styles.kpiLabel}>{label}</div>
      <div className={typeof value === 'number' ? styles.kpiValue : styles.kpiValueSmall}>
        {value}
      </div>
      {subtitle && <div className={styles.kpiSubtitle}>{subtitle}</div>}
    </div>
  );
}

export default KPICard;
