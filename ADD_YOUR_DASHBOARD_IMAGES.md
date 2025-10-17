# 📸 How to Add Your Oracle Samuel Dashboard Images

## 🎯 Quick Setup Instructions

To display your beautiful Oracle Samuel dashboard mockup images, follow these steps:

---

## 📁 Step 1: Save Your Images

1. **Save both dashboard images** to your project folder:
   ```
   Linear_regression APP/
   └── assets/
       ├── oracle_dashboard_1.jpg  (First laptop image)
       └── oracle_dashboard_2.jpg  (Second laptop image)
   ```

2. **Create the assets folder** if it doesn't exist:
   ```bash
   mkdir assets
   ```

3. **Name your images**:
   - First image (charts & graphs): `oracle_dashboard_1.jpg`
   - Second image (data analysis): `oracle_dashboard_2.jpg`

---

## 🔧 Step 2: Update app.py

Add this code to display your images in the hero section.

Replace the current dashboard preview section (around line 202-216) with:

```python
# Dashboard Preview Images
st.markdown("""
    <div style="text-align: center; margin: 2rem 0 1rem 0;">
        <p style="color: #F3E5AB; font-size: 1.1rem; font-family: 'Space Grotesk', sans-serif;">
            LIVE DASHBOARD PREVIEW
        </p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    try:
        st.image("assets/oracle_dashboard_1.jpg", use_column_width=True, caption="📊 Real Estate Analytics Dashboard")
    except:
        st.markdown("""
            <div style="background: #1a2332; padding: 3rem 1rem; border-radius: 20px; border: 2px solid #D4AF37; text-align: center;">
                <div style="color: #F3E5AB; font-size: 1.3rem; margin-bottom: 0.5rem;">📊 Dashboard Preview</div>
                <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">Interactive Analytics</div>
            </div>
        """, unsafe_allow_html=True)

with col2:
    try:
        st.image("assets/oracle_dashboard_2.jpg", use_column_width=True, caption="📈 Data Analysis Interface")
    except:
        st.markdown("""
            <div style="background: #1a2332; padding: 3rem 1rem; border-radius: 20px; border: 2px solid #D4AF37; text-align: center;">
                <div style="color: #F3E5AB; font-size: 1.3rem; margin-bottom: 0.5rem;">📈 Analysis Tools</div>
                <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">Predictive Modeling</div>
            </div>
        """, unsafe_allow_html=True)
```

---

## 🌐 Alternative: Use Online Image URLs

If you prefer to host your images online:

1. **Upload to an image hosting service**:
   - [Imgur](https://imgur.com)
   - [Postimage](https://postimages.org)
   - [ImgBB](https://imgbb.com)

2. **Get direct image URLs** (must end with .jpg or .png)

3. **Use in app.py**:
```python
st.image("https://your-image-url.com/dashboard1.jpg", use_column_width=True)
st.image("https://your-image-url.com/dashboard2.jpg", use_column_width=True)
```

---

## ✅ Current Setup (Temporary Placeholders)

Right now, your app shows **placeholder cards** with icons because the images aren't loaded yet.

Once you add the images, they will display automatically!

---

## 🎨 Image Requirements

For best results, your images should be:
- ✅ **Format**: JPG or PNG
- ✅ **Size**: 1200-1600px width recommended
- ✅ **Aspect Ratio**: 16:10 or 16:9 (laptop screen ratio)
- ✅ **Quality**: High resolution for crisp display

---

## 🚀 Quick Test

After adding images:

1. **Save them** to `assets/` folder
2. **Refresh** Streamlit (CTRL+R in browser)
3. **See your dashboards** appear in the hero section!

---

## 📋 Checklist

- [ ] Create `assets/` folder
- [ ] Save first dashboard as `oracle_dashboard_1.jpg`
- [ ] Save second dashboard as `oracle_dashboard_2.jpg`
- [ ] Update app.py with image code
- [ ] Refresh browser
- [ ] Enjoy your beautiful dashboard previews!

---

## 💡 Pro Tip

Your dashboard images show:
1. **First image**: Real estate charts, bar graphs, pie charts
2. **Second image**: Line graphs, data panels, analytics

These will look amazing in your hero section! 🎉

---

**Need help? Just ask!** 😊

