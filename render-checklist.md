# Render Deployment Checklist

## ✅ Pre-Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `requirements.txt` includes all dependencies
- [ ] `Procfile` created with correct command
- [ ] `runtime.txt` specifies Python version
- [ ] Django settings configured for production
- [ ] Secret key generated

## 🚀 Render Setup Steps

### Step 1: Sign Up
- [ ] Go to [render.com](https://render.com)
- [ ] Sign up with GitHub account
- [ ] Authorize Render access

### Step 2: Create Web Service
- [ ] Click "New" → "Web Service"
- [ ] Connect CipherChat repository
- [ ] Configure settings:
  - [ ] Name: `cipherchat`
  - [ ] Environment: `Python 3`
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `gunicorn cipherchat_web.wsgi:application`

### Step 3: Environment Variables
- [ ] Add `SECRET_KEY=et6ch**35_z72gqn=6cqj4=vk0utc1yk0e%urw9%(#ij_vpg)v`
- [ ] Add `DEBUG=False`
- [ ] Add `ALLOWED_HOSTS=your-app-name.onrender.com` (update after deployment)

### Step 4: Deploy
- [ ] Click "Create Web Service"
- [ ] Wait for build to complete (2-5 minutes)
- [ ] Check logs for any errors
- [ ] Test the live URL

## 🔧 Post-Deployment

- [ ] Update `ALLOWED_HOSTS` with actual Render URL
- [ ] Test user registration
- [ ] Test message encryption/decryption
- [ ] Create admin user if needed
- [ ] Share the URL with others!

## 📋 Your Render URL

After deployment, your app will be available at:
`https://your-app-name.onrender.com`

## 🆘 If Something Goes Wrong

1. **Check the logs** in Render dashboard
2. **Verify environment variables** are set correctly
3. **Ensure all files** are committed to GitHub
4. **Check requirements.txt** has all dependencies
5. **Try manual redeploy** if needed

## 🎉 Success!

Once deployed, your CipherChat app will be accessible to anyone with the URL!
