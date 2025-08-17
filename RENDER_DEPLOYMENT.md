# Render Deployment Guide for CipherChat

## Quick Setup

### 1. Sign Up
- Go to [render.com](https://render.com)
- Sign up with GitHub account
- Authorize Render access

### 2. Create Web Service
- Click "New" → "Web Service"
- Connect your CipherChat GitHub repository
- Configure settings below

### 3. Service Configuration

**Basic Settings:**
- **Name**: `cipherchat`
- **Environment**: `Python 3`
- **Region**: Choose closest to users
- **Branch**: `main`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn cipherchat_web.wsgi:application`

### 4. Environment Variables

Add these in the "Environment" section:

```bash
SECRET_KEY=et6ch**35_z72gqn=6cqj4=vk0utc1yk0e%urw9%(#ij_vpg)v
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
```

**Important**: Replace `your-app-name.onrender.com` with your actual Render URL after deployment.

### 5. Advanced Settings

- **Auto-Deploy**: ✅ Enabled
- **Health Check Path**: `/`
- **Health Check Timeout**: `180`

## Deployment Process

1. **Build Phase** (2-5 minutes):
   - Installs Python dependencies
   - Collects static files
   - Sets up environment

2. **Deploy Phase** (1-2 minutes):
   - Starts Gunicorn server
   - Runs database migrations
   - Health checks

3. **Live**: Your app is accessible at `https://your-app-name.onrender.com`

## Troubleshooting

### Build Failures

**Issue**: "Module not found" errors
**Solution**: Check `requirements.txt` has all dependencies

**Issue**: "Permission denied" errors
**Solution**: Make sure all files are committed to GitHub

### Runtime Errors

**Issue**: "SECRET_KEY not set"
**Solution**: Add SECRET_KEY environment variable

**Issue**: "ALLOWED_HOSTS" errors
**Solution**: Update ALLOWED_HOSTS with your Render URL

**Issue**: "Database connection" errors
**Solution**: Render provides SQLite by default, no additional setup needed

### Common Error Messages

```
Error: No module named 'django'
```
→ Check requirements.txt includes Django

```
Error: SECRET_KEY must not be empty
```
→ Add SECRET_KEY environment variable

```
Error: DisallowedHost at /
```
→ Update ALLOWED_HOSTS with your Render domain

## Post-Deployment

### 1. Test Your App
- Visit your Render URL
- Test user registration
- Test message encryption/decryption

### 2. Create Admin User
```bash
# In Render shell or locally with DATABASE_URL
python manage.py createsuperuser
```

### 3. Monitor Logs
- Go to your service dashboard
- Click "Logs" tab
- Monitor for errors

### 4. Custom Domain (Optional)
- Go to Settings → Custom Domains
- Add your domain
- Update ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS

## Render Free Tier Limits

- **750 hours/month** (enough for 24/7 uptime)
- **512 MB RAM**
- **Shared CPU**
- **Sleep after 15 minutes** of inactivity (wakes on request)

## Cost Optimization

- Free tier is sufficient for demos and small projects
- Paid plans start at $7/month for always-on service
- Consider paid plan for production use

## Security Notes

- Render provides automatic HTTPS
- Environment variables are encrypted
- Static files served via CDN
- Database backups available on paid plans

## Support

- Render documentation: https://render.com/docs
- Community forum: https://community.render.com
- Email support for paid plans

## Quick Commands

**Check deployment status:**
- View logs in Render dashboard

**Restart service:**
- Click "Manual Deploy" in dashboard

**Update environment variables:**
- Go to Environment tab and modify

**Scale service:**
- Available on paid plans
