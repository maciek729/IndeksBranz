import styles from '../css/CategoryCard.module.css';

interface CategoryCardProps {
  category: string;
  label: string;
  count: number;
  color: string;
}

function CategoryCard({ category, label, count, color }: CategoryCardProps) {
  return (
    <div className={styles.categoryCard}>
      <div className={styles.categoryBadge} style={{ backgroundColor: color }}>
        {category}
      </div>
      <div className={styles.categoryLabel}>{label}</div>
      <div className={styles.categoryCount}>{count} branż</div>
    </div>
  );
}

export default CategoryCard;
