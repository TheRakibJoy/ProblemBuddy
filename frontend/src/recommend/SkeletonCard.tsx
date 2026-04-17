export function SkeletonCard() {
  return (
    <div className="card h-100 shadow-sm" aria-hidden="true">
      <div className="skeleton" style={{ height: 80 }} />
      <div className="card-body">
        <div className="skeleton mb-2" style={{ height: 20, width: "60%" }} />
        <div className="skeleton mb-3" style={{ height: 16, width: "40%" }} />
        <div className="d-flex gap-1 flex-wrap mb-3">
          <div className="skeleton" style={{ height: 20, width: 50 }} />
          <div className="skeleton" style={{ height: 20, width: 70 }} />
          <div className="skeleton" style={{ height: 20, width: 40 }} />
        </div>
        <div className="skeleton" style={{ height: 38, width: "100%" }} />
      </div>
    </div>
  );
}
