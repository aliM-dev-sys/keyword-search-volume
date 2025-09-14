# Deployment Guide for Coolify + Hetzner

## 🚀 Quick Deployment Steps

### 1. GitHub Repository Setup
1. Create a new repository on GitHub
2. Push your code to the repository
3. Make sure all files are committed

### 2. Coolify Configuration

#### In Coolify Dashboard:
1. **Create New Application**
   - Source: GitHub
   - Repository: Your keyword-search-volume repo
   - Branch: main/master

2. **Build Settings**
   - Build Pack: Docker
   - Dockerfile: `./Dockerfile`
   - Build Context: `.`

3. **Environment Variables**
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   PORT=5000
   ```

4. **Port Configuration**
   - Internal Port: `5000`
   - External Port: `80` (or your preferred port)

### 3. Domain Configuration
- Set up your domain in Coolify
- Configure SSL certificate (Let's Encrypt)
- Point your domain to the Coolify server

## 📁 Files Added for Deployment

### Core Files:
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Local development
- `coolify.yml` - Coolify-specific config
- `gunicorn.conf.py` - Production WSGI server
- `.dockerignore` - Exclude unnecessary files

### Configuration:
- `env.example` - Environment variables template
- `DEPLOYMENT.md` - This guide

## 🔧 Production Optimizations

### 1. Gunicorn Configuration
- **Workers**: CPU cores × 2 + 1
- **Timeout**: 30 seconds
- **Max Requests**: 1000 (prevents memory leaks)
- **Keepalive**: 2 seconds

### 2. Security Features
- Non-root user in container
- Health checks enabled
- CORS properly configured
- Input validation and sanitization

### 3. Performance Features
- Gunicorn WSGI server
- Optimized Docker layers
- Proper caching headers
- Rate limiting protection

## 🌐 API Endpoints After Deployment

### Production URLs:
- **Health Check**: `https://yourdomain.com/api/health`
- **Search Volume**: `https://yourdomain.com/api/search-volume`
- **Web Interface**: `https://yourdomain.com/`

### n8n Integration:
```json
POST https://yourdomain.com/api/search-volume
Content-Type: application/json

{
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
  "geo": "US",
  "startTime": "2025-08-01T00:00:00.000Z",
  "endTime": "2025-08-31T00:00:00.000Z"
}
```

## 📊 Monitoring & Health Checks

### Health Check Endpoint:
```bash
curl https://yourdomain.com/api/health
```

Response:
```json
{
  "status": "healthy",
  "service": "keyword-search-volume-api",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### Docker Health Check:
- Checks every 30 seconds
- 30-second timeout
- 3 retries before marking unhealthy
- 5-second start period

## 🔍 Troubleshooting

### Common Issues:

1. **Port Not Accessible**
   - Check Coolify port configuration
   - Verify firewall settings on Hetzner
   - Ensure internal port is 5000

2. **Build Failures**
   - Check Dockerfile syntax
   - Verify all dependencies in requirements.txt
   - Check build logs in Coolify

3. **CORS Errors**
   - Verify Flask-CORS is installed
   - Check CORS configuration in app.py
   - Test with proper headers

4. **Rate Limiting**
   - Google Trends has rate limits
   - Implement delays between requests
   - Monitor API usage

### Debug Mode:
Set environment variable:
```
FLASK_DEBUG=True
```

## 📈 Scaling Considerations

### For High Traffic:
1. **Horizontal Scaling**: Deploy multiple instances
2. **Load Balancer**: Use Coolify's load balancing
3. **Caching**: Implement Redis for result caching
4. **Database**: Store results for repeated queries

### Resource Requirements:
- **Minimum**: 512MB RAM, 1 CPU core
- **Recommended**: 1GB RAM, 2 CPU cores
- **High Traffic**: 2GB+ RAM, 4+ CPU cores

## 🔐 Security Best Practices

1. **Environment Variables**: Never commit secrets
2. **HTTPS**: Always use SSL certificates
3. **Rate Limiting**: Implement request throttling
4. **Input Validation**: Sanitize all inputs
5. **Error Handling**: Don't expose sensitive errors

## 📝 Post-Deployment Checklist

- [ ] Health check endpoint responds
- [ ] API endpoints work with n8n
- [ ] SSL certificate is active
- [ ] Domain is properly configured
- [ ] Environment variables are set
- [ ] Monitoring is working
- [ ] Error logs are accessible

## 🆘 Support

If you encounter issues:
1. Check Coolify logs
2. Verify environment variables
3. Test health endpoint
4. Check Hetzner server status
5. Review this deployment guide
