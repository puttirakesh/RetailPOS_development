export default function LoadingBlock({ label = "Loading…" }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 gap-3 text-base-content/50">
      <span className="loading loading-spinner loading-md text-primary" />
      <p className="text-sm animate-[softPulse_1.6s_ease-in-out_infinite]">
        {label}
      </p>
    </div>
  );
}