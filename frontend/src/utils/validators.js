export function isValidCoordinate(lat, lng) {
  return lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180
}
