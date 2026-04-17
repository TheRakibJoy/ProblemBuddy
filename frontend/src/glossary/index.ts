export const TAG_GLOSSARY: Record<string, string> = {
  dp: "Dynamic programming — break a problem into overlapping subproblems.",
  graphs: "Graph traversal and algorithms (BFS, DFS, shortest paths, etc.).",
  dfs: "Depth-first search over graphs or trees.",
  bfs: "Breadth-first search, often for shortest paths in unweighted graphs.",
  math: "Number theory, combinatorics, modular arithmetic.",
  "number theory": "Divisibility, primes, modular arithmetic.",
  greedy: "Make locally-optimal choices that prove globally optimal.",
  "binary search": "Decide by halving the search space each step.",
  implementation: "Careful coding with attention to edge cases.",
  "data structures": "Segment/Fenwick trees, heaps, DSUs, tries, etc.",
  strings: "Pattern matching, hashing, KMP, Z-function.",
  "two pointers": "Sweep two indices over a sequence or sorted array.",
  sortings: "Problem reduces once data is sorted.",
  combinatorics: "Counting arrangements, stars and bars, inclusion–exclusion.",
  geometry: "Computational geometry primitives and techniques.",
  "brute force": "Try candidate solutions directly when the search space is small.",
  bitmasks: "Use bitwise operations to represent subsets or state.",
  constructive: "Design an object that satisfies the constraints.",
  "divide and conquer": "Split into independent subproblems and combine results.",
  flows: "Max-flow / min-cut algorithms.",
  interactive: "Query an online grader; communication-bounded.",
  probabilities: "Expected value / randomized analysis.",
};

export function describeTag(tag: string): string {
  return TAG_GLOSSARY[tag.toLowerCase()] ?? `Codeforces topic: ${tag}`;
}
