import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { fetchProfileSummary } from "../api/endpoints";
import { ChangeHandleModal } from "./ChangeHandleModal";
import { TierLadder } from "./TierLadder";
import { WeakTagsChart } from "./WeakTagsChart";

export function ProfilePage() {
  const [editing, setEditing] = useState(false);
  const { data, isLoading, isError } = useQuery({
    queryKey: ["profile-summary"],
    queryFn: fetchProfileSummary,
  });

  if (isLoading) {
    return (
      <div className="row justify-content-center">
        <div className="col-md-10">
          <div className="skeleton" style={{ height: 180 }} />
        </div>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="alert alert-warning text-center">
        Could not load your profile. Try refreshing the page.
      </div>
    );
  }

  return (
    <div className="row justify-content-center">
      <div className="col-md-10">
        <div className="card shadow-sm mb-3">
          <div className="row g-0">
            <div className="col-md-4 bg-info text-white text-center p-4 rounded-start">
              {data.photo && (
                <img
                  src={data.photo}
                  alt={data.cf_handle ?? data.username}
                  className="rounded-circle img-fluid"
                  style={{ maxWidth: 150 }}
                />
              )}
              <h2 className="mt-3">{data.cf_handle ?? data.username}</h2>
              <p className="mb-2">{data.max_rank || "unrated"}</p>
              <button
                type="button"
                className="btn btn-sm btn-light"
                onClick={() => setEditing(true)}
              >
                Change handle
              </button>
            </div>
            <div className="col-md-8 p-4">
              <h3 className="text-center">Information</h3>
              <hr className="w-25 mx-auto" />
              <div className="row mb-3">
                <div className="col-md-6">
                  <p className="fw-bold mb-1">Email</p>
                  <p className="text-muted">{data.email || "—"}</p>
                </div>
                <div className="col-md-6">
                  <p className="fw-bold mb-1">Max rating</p>
                  <p className="text-muted">{data.max_rating || "—"}</p>
                </div>
              </div>

              <TierLadder
                tiers={data.tiers}
                currentFloor={data.current_floor}
                nextTarget={data.next_target}
                maxRating={data.max_rating}
              />

              <h3 className="text-center">Your weak areas</h3>
              <hr className="w-25 mx-auto" />
              <WeakTagsChart weakTags={data.weak_tags} />
            </div>
          </div>
        </div>
      </div>

      {editing && (
        <ChangeHandleModal
          currentHandle={data.cf_handle}
          onClose={() => setEditing(false)}
        />
      )}
    </div>
  );
}
