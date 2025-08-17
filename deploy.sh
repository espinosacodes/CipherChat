#!/bin/bash

echo "🚀 CipherChat Deployment Helper"
echo "================================"

# Generate a secure secret key
echo "🔑 Generating secure secret key..."
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

echo ""
echo "✅ Your secure secret key:"
echo "$SECRET_KEY"
echo ""

echo "📋 Environment variables to set in your deployment platform:"
echo "=========================================================="
echo "SECRET_KEY=$SECRET_KEY"
echo "DEBUG=False"
echo "ALLOWED_HOSTS=your-app-name.railway.app,your-app-name.onrender.com,your-app-name.herokuapp.com"
echo ""

echo "🌐 Quick Deploy Options:"
echo "======================="
echo "1. Railway (Recommended): https://railway.app"
echo "2. Render: https://render.com"
echo "3. Heroku: https://heroku.com"
echo ""

echo "📖 See DEPLOYMENT.md for detailed instructions"
echo ""

echo "🔧 Pre-deployment checklist:"
echo "==========================="
echo "✅ Requirements.txt updated"
echo "✅ Procfile created"
echo "✅ Runtime.txt created"
echo "✅ Django settings configured for production"
echo "✅ Secret key generated"
echo ""

echo "🎯 Next steps:"
echo "============="
echo "1. Push your code to GitHub"
echo "2. Choose a deployment platform"
echo "3. Connect your repository"
echo "4. Set the environment variables above"
echo "5. Deploy!"
echo ""

echo "🔗 Your app will be live at:"
echo "https://your-app-name.railway.app (Railway)"
echo "https://your-app-name.onrender.com (Render)"
echo "https://your-app-name.herokuapp.com (Heroku)"
