# CipherChat Deployment Guide

This guide will help you deploy your CipherChat web application to make it accessible to others.

## Quick Deploy Options

### 1. Railway (Recommended - Easiest)

**Steps:**
1. Go to [railway.app](https://railway.app) and sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your CipherChat repository
4. Railway will automatically detect it's a Django app
5. Add these environment variables in Railway dashboard:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.railway.app
   ```
6. Deploy! Your app will be available at `https://your-app-name.railway.app`

### 2. Render (Great Free Option)

**Steps:**
1. Go to [render.com](https://render.com) and sign up
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: cipherchat
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn cipherchat_web.wsgi:application`
5. Add environment variables:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   ```
6. Deploy! Your app will be at `https://your-app-name.onrender.com`

### 3. Heroku (Production Ready)

**Steps:**
1. Install Heroku CLI and sign up at [heroku.com](https://heroku.com)
2. Run these commands:
   ```bash
   heroku create your-cipherchat-app
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```
3. Your app will be at `https://your-app-name.herokuapp.com`

## Environment Variables

Set these in your deployment platform:

```bash
# Required
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Optional (for production database)
DATABASE_URL=postgresql://user:password@host:port/database

# Security (for HTTPS)
CSRF_TRUSTED_ORIGINS=https://your-domain.com
SECURE_SSL_REDIRECT=True
```

## Generate a Secure Secret Key

Run this Python command to generate a secure secret key:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Database Setup

For production, consider using PostgreSQL instead of SQLite:

### Railway/Render/Heroku
- These platforms automatically provide PostgreSQL
- The `DATABASE_URL` will be set automatically

### Manual PostgreSQL Setup
1. Install PostgreSQL
2. Create a database
3. Set `DATABASE_URL=postgresql://user:password@localhost:5432/cipherchat`

## Static Files

The app is configured to serve static files with WhiteNoise. For production:

```bash
python manage.py collectstatic
```

## Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use a strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Enable HTTPS (automatic on most platforms)
- [ ] Set up proper CSRF settings
- [ ] Use environment variables for sensitive data

## Troubleshooting

### Common Issues:

1. **Static files not loading**: Run `python manage.py collectstatic`
2. **Database errors**: Check `DATABASE_URL` environment variable
3. **CSRF errors**: Add your domain to `CSRF_TRUSTED_ORIGINS`
4. **Import errors**: Make sure all packages in `requirements.txt` are installed

### Logs:
- Railway: View logs in the dashboard
- Render: Check the "Logs" tab
- Heroku: `heroku logs --tail`

## Custom Domain (Optional)

After deployment, you can add a custom domain:

1. **Railway**: Go to Settings → Domains
2. **Render**: Go to Settings → Custom Domains
3. **Heroku**: `heroku domains:add yourdomain.com`

Remember to update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` with your custom domain.

## Cost Comparison

- **Railway**: Free tier available, then $5/month
- **Render**: Free tier available, then $7/month
- **Heroku**: $5/month minimum
- **VPS**: $5-20/month depending on provider

## Next Steps

1. Choose a deployment platform
2. Follow the steps above
3. Test your deployed application
4. Share the URL with others!

Your CipherChat app will be accessible to anyone with the URL once deployed.
