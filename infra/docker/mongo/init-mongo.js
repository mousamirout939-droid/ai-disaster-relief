// Runs once on first container start (docker-entrypoint-initdb.d convention).
// Creates the application database and a least-privilege app user.
db = db.getSiblingDB("disaster_relief_platform");

db.createUser({
  user: "relief_app",
  pwd: "change-me-in-production",
  roles: [{ role: "readWrite", db: "disaster_relief_platform" }],
});

db.createCollection("users");
db.createCollection("incidents");
db.createCollection("shelters");
db.createCollection("inventory_logs");
db.createCollection("alerts");
db.createCollection("aid_requests");
db.createCollection("audit_logs");
db.createCollection("chat_sessions");

print("disaster_relief_platform initialized with base collections.");
