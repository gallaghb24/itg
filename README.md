# Intelligent Transformation Group Website

A modern, minimalist one-page website for ITG - designed for senior operations, marketing and transformation leaders.

## Quick Start

### Hosting on GitHub Pages

1. Create a new repository on GitHub (e.g., `itg-website`)
2. Upload all files from this project
3. Go to Settings → Pages
4. Select "Deploy from branch" and choose `main` branch
5. Your site will be live at `https://yourusername.github.io/itg-website/`

### Custom Domain Setup (Optional)

If you want to use a custom domain like `intelligenttransformation.group`:

1. Add a `CNAME` file to your repository with your domain name
2. In your domain registrar (e.g., Namecheap, GoDaddy):
   - Add an A record pointing to GitHub's IP addresses:
     - 185.199.108.153
     - 185.199.109.153
     - 185.199.110.153
     - 185.199.111.153
   - Or add a CNAME record pointing to `yourusername.github.io`
3. In GitHub Settings → Pages, add your custom domain
4. Wait for DNS propagation (can take up to 24 hours)

## File Structure

```
itg-website/
├── index.html          # Main HTML file with all content sections
├── styles.css          # All styling with coral accent color scheme
├── script.js           # Smooth scrolling, animations, form handling
├── favicon.svg         # ITG logo favicon
└── README.md          # This file
```

## Features

✓ **Fully Responsive** - Works perfectly on mobile, tablet, and desktop
✓ **Smooth Scrolling** - Navigation links smoothly scroll to sections
✓ **Scroll Animations** - Elements fade in as you scroll
✓ **Mobile Menu** - Collapsible navigation for mobile devices
✓ **Contact Form** - Ready for Netlify Forms (or can be adapted)
✓ **Fast Loading** - Optimized performance with no external dependencies
✓ **SEO Optimized** - Proper meta tags, semantic HTML, and descriptions

## Design System

### Colors
- **Coral Accent**: #FF6B6B
- **Dark Background**: #1A1A1A
- **Light Background**: #F8F9FA
- **Text**: #1F2937

### Typography
- **Font**: System font stack (San Francisco, Segoe UI, Roboto)
- **Scale**: Fluid typography using clamp() for responsive sizing
- **Spacing**: Consistent scale from 0.5rem to 8rem

## Customization

### Changing Colors
Edit the CSS variables in `styles.css`:
```css
:root {
    --coral: #FF6B6B;        /* Your accent color */
    --dark: #1A1A1A;         /* Dark sections background */
    --light: #FFFFFF;        /* Light sections background */
}
```

### Updating Content
All content is in `index.html`. Each section is clearly commented.

### Form Setup

**For Netlify hosting:**
The form is already configured. Just deploy to Netlify and it will work automatically.

**For GitHub Pages:**
You'll need to:
1. Use a form service like Formspree, Basin, or Getform
2. Update the form action in `index.html`

Example with Formspree:
```html
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
```

## Browser Support

✓ Chrome (last 2 versions)
✓ Firefox (last 2 versions)
✓ Safari (last 2 versions)
✓ Edge (last 2 versions)

## Performance

- No external dependencies (no jQuery, no frameworks)
- Optimized animations using CSS transforms
- Debounced scroll events for better performance
- Minimal JavaScript footprint

## SEO & Social

The site includes:
- Meta descriptions for search engines
- Open Graph tags for social media sharing
- Twitter Card meta tags
- Semantic HTML structure
- Proper heading hierarchy

## Local Development

Simply open `index.html` in your browser. No build process required.

For a local server (optional):
```bash
python -m http.server 8000
# or
npx serve
```

## Deployment Checklist

- [ ] Update email address in footer
- [ ] Configure form submission endpoint
- [ ] Add your domain to CNAME file (if using custom domain)
- [ ] Test all navigation links
- [ ] Test form submission
- [ ] Check mobile responsiveness
- [ ] Test in different browsers
- [ ] Enable HTTPS in GitHub Pages settings

## Support

For questions about the website design or code, refer to:
- GitHub Pages: https://docs.github.com/pages
- HTML/CSS/JavaScript: https://developer.mozilla.org/

## License

This website template is provided as-is for Intelligent Transformation Group.

---

**Tagline for SEO/Social**: 
Intelligent Transformation Group – Transforming how work gets done through operational design, automation and AI.

**Meta Description**:
We help marketing organisations and creative operations re-engineer workflows through intelligent automation, AI and operational design for faster, leaner delivery.
