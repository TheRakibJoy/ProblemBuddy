import { useIsFetching, useIsMutating } from "@tanstack/react-query";

export function TopProgress() {
  const fetching = useIsFetching();
  const mutating = useIsMutating();
  const active = fetching + mutating > 0;
  return (
    <div
      className="position-fixed top-0 start-0 end-0"
      style={{ height: 3, zIndex: 1090, pointerEvents: "none" }}
      aria-hidden
    >
      <div
        className="bg-primary"
        style={{
          height: "100%",
          width: active ? "85%" : "0%",
          transition: active ? "width 1.2s ease-out" : "width 200ms ease-out, opacity 400ms",
          opacity: active ? 1 : 0,
        }}
      />
    </div>
  );
}
