# Admin Setup Guide

## Production Admin Setup

### Method 1: Database Admin User (Recommended)

1. Run the admin setup script on your production server:
   ```bash
   cd backend
   poetry run python setup_admin.py
   ```

2. Save the generated credentials securely

3. Login to the application using the provided email and password

### Method 2: Environment Variables

Set these environment variables in your production deployment:

```bash
# Option A: Use login credentials
ADMIN_LOGIN_USER=admin@echostor.com
ADMIN_LOGIN_PASSWORD=your-secure-password

# Option B: Use email and password hash
ADMIN_EMAIL=aadish.bahati@echostor.com
ADMIN_PASSWORD_HASH=$2b$12$your-bcrypt-hash
```

### Verification

1. Access the admin dashboard at `/admin`
2. Verify all admin API endpoints work:
   - `/api/admin/dashboard/stats`
   - `/api/admin/users`
   - `/api/admin/reports`
   - `/api/admin/alerts`
   - `/api/admin/consultations`

### Troubleshooting

- **403 Errors**: Check admin credentials and is_admin field in database
- **500 Errors**: Check database connection and environment variables
- **CORS Errors**: Verify ALLOWED_ORIGINS includes your domain
