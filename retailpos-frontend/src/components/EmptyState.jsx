export default function EmptyState({ title, hint }) {
  return (
    <div className="text-center py-16 px-4 text-base-content/50">
      <div className="mx-auto mb-3 w-12 h-12 rounded-2xl bg-base-200 flex items-center justify-center text-lg opacity-60">
        ∅
      </div>
      <p className="font-medium text-base-content/70">{title}</p>
      {hint && <p className="text-sm mt-1 max-w-sm mx-auto">{hint}</p>}
    </div>
  );
}