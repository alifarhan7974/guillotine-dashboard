export default function WeekNavigator({ week, canGoPrevious, canGoNext, onPrevious, onNext }) {
  return <div className="week-navigator" aria-label="Week navigation">
    <button type="button" onClick={onPrevious} disabled={!canGoPrevious}>← Previous</button>
    <strong>Week {week}</strong>
    <button type="button" onClick={onNext} disabled={!canGoNext}>Next →</button>
  </div>;
}
