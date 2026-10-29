export default function WeekNavigator({ week, canGoPrevious, canGoNext, onPrevious, onNext }) {
  return (
    <nav className="week-navigator" aria-label="Week navigation">
      <button type="button" onClick={onPrevious} disabled={!canGoPrevious}>
        <span aria-hidden="true">←</span> Previous
      </button>
      <p><span>Scoreboard</span><strong>Week {week}</strong></p>
      <button type="button" onClick={onNext} disabled={!canGoNext}>
        Next <span aria-hidden="true">→</span>
      </button>
    </nav>
  );
}
