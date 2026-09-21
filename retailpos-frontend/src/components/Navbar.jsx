import { Menu, Bell, Search } from "lucide-react";

export default function Navbar({ title, onMenuClick }) {
  return (
    <header className="sticky top-0 z-30 glass-nav border-b border-base-300/60">
      <div className="flex items-center gap-3 px-4 lg:px-6 h-14">
        <button
          type="button"
          className="btn btn-ghost btn-sm btn-square lg:hidden"
          onClick={onMenuClick}
          aria-label="Open menu"
        >
          <Menu size={20} />
        </button>

        <div className="flex-1 min-w-0">
          <h1 className="text-base lg:text-lg font-semibold tracking-tight truncate">
            {title}
          </h1>
        </div>

        <div className="hidden md:flex items-center gap-2 max-w-xs w-full">
          <label className="input input-sm input-bordered flex items-center gap-2 w-full bg-base-200/40 border-base-300/50">
            <Search size={14} className="opacity-40" />
            <input
              type="text"
              className="grow text-sm bg-transparent"
              placeholder="Quick search…"
              disabled
            />
          </label>
        </div>

        <button
          type="button"
          className="btn btn-ghost btn-sm btn-square relative"
          aria-label="Notifications"
        >
          <Bell size={18} />
          <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full bg-primary ring-2 ring-base-100" />
        </button>
      </div>
    </header>
  );
}