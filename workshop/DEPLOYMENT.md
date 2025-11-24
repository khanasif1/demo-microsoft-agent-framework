# 🚀 Workshop Deployment Guide

This guide explains how to publish your Microsoft Agent Framework workshop to GitHub Pages.

## 📋 Prerequisites

- Repository pushed to GitHub
- GitHub account with repository access
- Workshop files in the `workshop/` folder

## 🌐 Publishing to GitHub Pages

### Method 1: GitHub Actions (Automatic - Recommended)

✅ **Good news!** The GitHub Actions workflow is already configured in this repository.

1. **Enable GitHub Pages**
   - Go to your repository settings on GitHub
   - Navigate to **Settings → Pages**
   - Under **Source**, select **GitHub Actions**
   - Click **Save**

2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy workshop to GitHub Pages"
   git push origin main
   ```

3. **Monitor Deployment**
   - Go to **Actions** tab in your GitHub repository
   - Watch the "Deploy Workshop to GitHub Pages" workflow run
   - It should complete in 1-2 minutes

4. **Access Your Workshop**
   - Visit: `https://YOUR_USERNAME.github.io/demo-microsoft-agent-framework/`
   - The workshop will be automatically available at the root URL

**Note:** The workflow file is located at `.github/workflows/pages.yml` and deploys the `workshop/` folder contents.

### Method 2: Manual (Branch-based)

1. **Push Workshop to GitHub**
   ```bash
   git add workshop/
   git commit -m "Add Microsoft Agent Framework workshop"
   git push origin main
   ```

2. **Enable GitHub Pages**
   - Go to repository **Settings → Pages**
   - Under **Source**, select **Deploy from a branch**
   - Choose **main** branch
   - Select **/ (root)** or **/workshop** folder
   - Click **Save**

3. **Wait for Deployment**
   - GitHub will build and deploy (takes 1-2 minutes)
   - Check **Actions** tab for progress

4. **Access Your Workshop**
   - URL will be: `https://YOUR_USERNAME.github.io/demo-microsoft-agent-framework/workshop/`

## 🔧 Configuration

### Custom Domain (Optional)

If you want a custom domain:

1. **Create CNAME file**
   ```bash
   echo "workshop.yourdomain.com" > workshop/CNAME
   ```

2. **Configure DNS**
   - Add CNAME record pointing to `YOUR_USERNAME.github.io`

3. **Enable in GitHub Settings**
   - Settings → Pages → Custom domain
   - Enter your domain and verify

## 🎨 Workshop Structure

Ensure your `workshop/` folder has this structure:

```
workshop/
├── index.html              # Landing page
├── prerequisites.html
├── environment-setup.html
├── azure-setup.html
├── code-walkthrough.html
├── running-app.html
├── troubleshooting.html
├── README.md
├── DEPLOYMENT.md          # This file
├── _config.yml            # Jekyll config
└── assets/
    └── styles.css
```

## ✅ Verification

After deployment:

1. **Check Links**
   - Visit your GitHub Pages URL
   - Test all navigation links
   - Verify CSS loads correctly

2. **Test on Multiple Devices**
   - Desktop browser
   - Mobile device
   - Tablet

3. **Validate HTML**
   - Use [W3C Validator](https://validator.w3.org/)

## 🐛 Troubleshooting

### Issue: 404 Page Not Found

**Solution:**
- Ensure `index.html` exists in workshop folder
- Check GitHub Pages source settings
- Wait 2-3 minutes for deployment

### Issue: CSS Not Loading

**Solution:**
- Check `assets/styles.css` path is correct
- Ensure relative paths in HTML: `href="assets/styles.css"`
- Clear browser cache

### Issue: Links Broken

**Solution:**
- Use relative paths (not absolute)
- Example: `href="prerequisites.html"` not `href="/workshop/prerequisites.html"`

### Issue: Build Fails

**Solution:**
- Check GitHub Actions logs
- Verify no special characters in filenames
- Ensure all files are committed

## 🔒 Security

### Environment Variables

The workshop requires `.env` file with:
```
AZURE_AI_PROJECT_ENDPOINT=your_endpoint
AZURE_AI_MODEL_DEPLOYMENT_NAME=your_deployment
```

**Important:**
- ✅ `.env` is in `.gitignore` (never commit credentials)
- ✅ Workshop explains how students create their own `.env`
- ✅ No credentials are published to GitHub Pages

### Best Practices

- Never commit `.env` files
- Use placeholder values in documentation
- Instruct students to create their own Azure resources
- Don't include API keys or secrets in HTML

## 📊 Analytics (Optional)

Add Google Analytics to track workshop usage:

1. **Get Tracking ID** from Google Analytics

2. **Add to HTML** (before `</head>`):
   ```html
   <!-- Google Analytics -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());
     gtag('config', 'G-XXXXXXXXXX');
   </script>
   ```

## 🔄 Updating the Workshop

To update content:

```bash
# 1. Make changes to HTML files
# 2. Test locally
open workshop/index.html

# 3. Commit and push
git add workshop/
git commit -m "Update workshop content"
git push origin main

# 4. GitHub Pages will auto-redeploy (if using Actions)
```

## 📱 Social Sharing

After deployment, share your workshop:

**Update README.md with:**
```markdown
🌐 **Live Workshop:** https://YOUR_USERNAME.github.io/demo-microsoft-agent-framework/
```

**Share on social media:**
- Twitter: "Just published a hands-on #MicrosoftAgentFramework workshop! 🤖"
- LinkedIn: Announce your educational resource
- Dev.to: Write a blog post about the workshop

## 🎓 Workshop Metrics

Track success with:
- GitHub Stars
- Page views (GitHub Insights or Analytics)
- Issues/feedback
- Community contributions

## 📝 Next Steps

After deployment:

1. ✅ Test all workshop modules
2. ✅ Share with community
3. ✅ Collect feedback
4. ✅ Iterate and improve
5. ✅ Add more advanced modules

## 🤝 Contributing

Encourage contributions:
- Fork and PR workflow
- Issue templates for bug reports
- Feature request template
- Contributor guidelines

## 📄 License

Ensure workshop has proper licensing:
- MIT License (included in repository)
- Attribution for borrowed content
- Links to original sources

---

**Deployment Checklist:**

- [ ] Workshop files in `workshop/` folder
- [ ] All HTML files created and tested
- [ ] CSS file properly linked
- [ ] Navigation links working
- [ ] `.env` in `.gitignore`
- [ ] README.md updated with live URL
- [ ] GitHub Pages enabled
- [ ] Deployment successful
- [ ] Tested on multiple devices
- [ ] Shared with community

**Ready to deploy?** Follow Method 1 (GitHub Actions) for automatic deployments! 🚀
