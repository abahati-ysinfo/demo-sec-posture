# Database Migrations

This directory contains SQL migration scripts for the EchoStor Security Posture Assessment database.

## How to Apply Migrations

### On Fly.io Production

```bash
# Connect to the database via Fly.io
flyctl postgres connect -a echostor-security-posture-tool-db

# Or use psql directly
flyctl proxy 5432 -a echostor-security-posture-tool-db
psql postgresql://postgres:password@localhost:5432/echostor_security_posture

# Run the migration
\i /path/to/migration.sql
```

### Using flyctl ssh

```bash
# SSH into the app container
flyctl ssh console -a echostor-security-posture-tool

# Connect to database and run migration
psql $DATABASE_URL -f /app/migrations/001_add_assessment_response_indexes.sql
```

## Migration History

| Migration | Date | Description |
|-----------|------|-------------|
| 001_add_assessment_response_indexes.sql | 2025-10-27 | Add indexes to assessment_responses table for performance optimization |

## Notes

- Always test migrations on a staging environment first
- Indexes are created with `IF NOT EXISTS` to allow safe re-running
- Monitor query performance after applying indexes
