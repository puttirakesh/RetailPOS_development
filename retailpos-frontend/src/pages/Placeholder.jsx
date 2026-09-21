import { Construction } from "lucide-react";
import { Link } from "react-router-dom";

export default function Placeholder({ name }) {
  return (
    <div className="card-premium p-12 text-center page-enter">
      <div className="mx-auto w-14 h-14 rounded-2xl bg-base-200 flex items-center justify-center mb-4">
        <Construction className="text-base-content/35" size={28} />
      </div>
      <h2 className="text-xl font-semibold">{name}</h2>
      <p className="text-sm text-base-content/50 mt-2 max-w-md mx-auto leading-relaxed">
        UI for this master lands in Phase 10. The API already works in Swagger /
        Postman.
      </p>
      <Link to="/masters/brands" className="btn btn-primary btn-sm mt-6 rounded-xl">
        Open Brands
      </Link>
    </div>
  );
}