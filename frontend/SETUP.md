# Frontend Installation & Setup

## 📦 Prerequisites
- Node.js 14+ 
- npm or yarn

## 🔧 Installation

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Create .env File
```bash
# Create .env file in frontend directory
REACT_APP_API_URL=http://localhost:5000
```

### 3. Start Development Server
```bash
npm start
```

Application will open at `http://localhost:3000`

## 📁 Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── Login.js
│   │   │   └── Login.css
│   │   └── Dashboard/
│   │       ├── Dashboard.js
│   │       ├── Dashboard.css
│   │       ├── CaseList.js
│   │       ├── CaseDetail.js
│   │       ├── Analytics.js
│   │       └── Analytics.css
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## 🎨 Styling

The application uses:
- CSS3 for styling
- CSS Grid and Flexbox for layouts
- Gradient backgrounds
- Responsive design

## 🔄 Component Communication

- State management using React Hooks
- Props drilling for data passing
- localStorage for token storage
- fetch API for backend communication

## 📊 Available Scripts

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Eject configuration
npm run eject
```

## 🌐 API Integration

All API calls to backend at `http://localhost:5000`

### Authentication Flow
1. User registers/logs in
2. Server returns JWT token
3. Token stored in localStorage
4. Token sent in Authorization header for protected routes

### Component Lifecycle

**Login.js**
- User registers/logs in
- Calls /api/auth/register or /api/auth/login
- Stores token and user data
- Navigates to Dashboard

**Dashboard.js**
- Loads user's cases from /api/cases
- Displays case list
- Allows case selection
- Shows analytics tabs

**CaseDetail.js**
- Shows selected case details
- Displays module buttons
- Passes selected module to Analytics component

**Analytics.js**
- Calls appropriate analytics endpoint based on moduleId
- Displays results in formatted cards
- Shows JSON output for debugging

## 📱 Responsive Design

The application is fully responsive:
- Mobile (< 768px)
- Tablet (768px - 1024px)
- Desktop (> 1024px)

## 🔐 Security

- JWT tokens stored in localStorage (consider secure cookie in production)
- HTTPS required in production
- Input validation on forms
- CORS headers from backend

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Serve Static Files
```bash
npm install -g serve
serve -s build
```

### Deploy to Netlify
```bash
npm run build
netlify deploy --prod --dir=build
```

### Deploy to Vercel
```bash
vercel
```

## 🐛 Debugging

### Browser DevTools
- F12 to open DevTools
- Console tab for errors
- Network tab to see API calls
- Application tab for localStorage

### React DevTools
- Install React DevTools extension
- Inspect component hierarchy
- Check props and state

## 📚 Additional Resources

- React Documentation: https://react.dev
- CSS Grid: https://css-tricks.com/snippets/css/complete-guide-grid/
- Flexbox: https://css-tricks.com/snippets/css/a-guide-to-flexbox/
