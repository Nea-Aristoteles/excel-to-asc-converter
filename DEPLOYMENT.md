# 🚀 Deployment Guide

This guide covers deploying the Excel to ASC Converter to various cloud platforms.

## 🌐 Render.com (Recommended)

Render is a modern cloud platform that makes deployment simple and offers a generous free tier.

### Prerequisites
- GitHub account with your repository
- Render account (free at [render.com](https://render.com))

### Step-by-Step Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add deployment configuration"
   git push origin main
   ```

2. **Connect to Render**
   - Go to [render.com](https://render.com) and sign up/login
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select your `excel-to-asc-converter` repository

3. **Configure Service**
   - **Name**: `excel-to-asc-converter` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Plan**: Free (or paid for better performance)

4. **Environment Variables** (Optional)
   - `SECRET_KEY`: Generate a secure random string
   - `FLASK_ENV`: `production`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (usually 2-5 minutes)
   - Your app will be available at `https://your-service-name.onrender.com`

### Automatic Deployments
Render automatically redeploys when you push to your main branch on GitHub.

## 🔧 Alternative Platforms

### Heroku
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Deploy: `git push heroku main`

### Railway
1. Connect GitHub repository at [railway.app](https://railway.app)
2. Select your repository
3. Railway auto-detects Python and deploys

### PythonAnywhere
1. Upload files to your account
2. Create web app with Flask
3. Configure WSGI file to point to your app

## 📊 Production Considerations

### Performance
- **Free Tier Limitations**: 
  - Render free tier sleeps after 15 minutes of inactivity
  - Cold starts take 10-30 seconds
  - Consider paid tier for production use

### Security
- Set a secure `SECRET_KEY` environment variable
- Enable HTTPS (automatic on Render)
- Consider rate limiting for production

### Monitoring
- Check Render dashboard for logs and metrics
- Set up health checks (already configured)
- Monitor file upload sizes and processing times

### File Storage
- Temporary files are automatically cleaned up
- For persistent storage, consider cloud storage services
- Current setup uses local temp files (suitable for most use cases)

## 🐛 Troubleshooting

### Common Issues

**Build Fails**
- Check Python version in `runtime.txt`
- Verify all dependencies in `requirements.txt`
- Check build logs in Render dashboard

**App Won't Start**
- Verify `Procfile` and start command
- Check for syntax errors in `app.py`
- Review application logs

**File Upload Issues**
- Ensure `MAX_CONTENT_LENGTH` is appropriate
- Check temporary file permissions
- Verify pandas/openpyxl installation

**Port Issues**
- Use `PORT` environment variable (handled automatically)
- Don't hardcode ports in production

### Getting Help
- Check Render documentation
- Review application logs
- Test locally first with `gunicorn --bind 0.0.0.0:8080 app:app`

## 📈 Scaling

### Horizontal Scaling
- Upgrade to paid Render plan for multiple instances
- Use load balancer for high traffic

### Vertical Scaling
- Increase memory/CPU on paid plans
- Optimize pandas operations for large files

### Caching
- Consider Redis for session storage
- Cache processed results if needed

## 🔄 CI/CD Pipeline

### GitHub Actions (Optional)
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Render
      run: echo "Render auto-deploys on push"
```

### Testing Before Deploy
```bash
# Test locally with production settings
export FLASK_ENV=production
gunicorn --bind 0.0.0.0:8080 app:app
```

## 📋 Deployment Checklist

- [ ] Repository pushed to GitHub
- [ ] All deployment files added (`Procfile`, `runtime.txt`, etc.)
- [ ] Dependencies updated in `requirements.txt`
- [ ] Environment variables configured
- [ ] Service created on Render
- [ ] Domain configured (if using custom domain)
- [ ] SSL/HTTPS enabled (automatic on Render)
- [ ] Health checks working
- [ ] File upload tested in production
- [ ] Error handling verified

Your Excel to ASC Converter is now ready for production deployment! 🎉 