export function tagAccent(tags: string[]): string {
  if (!tags.length) return "linear-gradient(135deg, #64748b 0%, #94a3b8 100%)";
  let hash = 0;
  for (const tag of tags) {
    for (let i = 0; i < tag.length; i++) hash = (hash * 31 + tag.charCodeAt(i)) & 0xffffffff;
  }
  const h1 = Math.abs(hash) % 360;
  const h2 = (h1 + 45) % 360;
  return `linear-gradient(135deg, hsl(${h1} 70% 55%) 0%, hsl(${h2} 70% 45%) 100%)`;
}
