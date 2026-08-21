export function formatDistance(km) {
  return km < 1 ? `${Math.round(km * 1000)}m` : `${km.toFixed(1)}km`
}

export function titleCase(str) {
  return str.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
}
