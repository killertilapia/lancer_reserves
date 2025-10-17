# Lancer Reserves Frontend

A Vue.js 3 application built with the Composition API, single file components, and Bootstrap 5 for styling.

## Features

- **Vue 3 with Composition API**: Modern reactive programming with `<script setup>` syntax
- **Single File Components**: All components use `.vue` files with template, script, and style sections
- **Bootstrap 5**: Responsive design with Bootstrap 5 components and utilities
- **Vite**: Fast development server and build tool
- **Bootstrap Icons**: Comprehensive icon library

## Project Structure

```
app/
├── src/
│   ├── components/
│   │   ├── NavBar.vue          # Navigation component
│   │   ├── ReservesDashboard.vue # Main dashboard component
│   │   └── AddReserveModal.vue   # Modal for adding reserves
│   ├── App.vue                 # Root component
│   └── main.js                 # Application entry point
├── index.html                  # HTML template
├── package.json               # Dependencies and scripts
├── vite.config.js             # Vite configuration
└── README.md                  # This file
```

## Getting Started

### Prerequisites

- Node.js (version 16 or higher)
- npm or yarn
- Backend API running (see backend documentation)

### Installation

1. Navigate to the app directory:
   ```bash
   cd app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure environment variables:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env to set your backend URL (default: http://localhost:8000)
   # VITE_API_BASE_URL=http://localhost:8000
   ```

### Development

1. Start the backend API (from project root):
   ```bash
   cd backend
   python -m uvicorn main:app --reload
   ```

2. Start the frontend development server:
   ```bash
   cd app
   npm run dev
   ```

The application will be available at `http://localhost:3000` and will connect to the backend API.

### Building for Production

Build the application for production:
```bash
npm run build
```

The built files will be in the `dist` directory.

### Preview Production Build

Preview the production build locally:
```bash
npm run preview
```

## Components Overview

### App.vue
The root component that sets up the main application structure and imports the navigation and dashboard components.

### NavBar.vue
A responsive navigation bar with Bootstrap styling that includes:
- Brand logo with icon
- Navigation links
- User dropdown menu
- Mobile-responsive toggle

### ReservesDashboard.vue
The main dashboard component featuring:
- Statistics cards showing reserve metrics
- Data table displaying reserves
- Add/Edit/Delete functionality
- Bootstrap-styled components

### AddReserveModal.vue
A modal component for adding new reserves with:
- Form validation
- Bootstrap form components
- Loading states
- Error handling

## Backend Integration

### GraphQL API

The frontend integrates with the FastAPI backend using GraphQL. The API service is located in `src/services/graphql.js` and provides:

**Available Queries:**
- `fetchReserves(type, skip, limit)` - List reserves with filtering
- `fetchReserveById(id)` - Get single reserve
- `fetchRandomReserves(count, type)` - Get random reserves
- `fetchReservesByLabel(label)` - Search by label

**Available Mutations:**
- `createReserve(input)` - Create new reserve
- `updateReserve(id, input)` - Update existing reserve
- `deleteReserve(id)` - Delete reserve

### Environment Configuration

The backend URL is configurable via environment variables:

```bash
# .env file
VITE_API_BASE_URL=http://localhost:8000
```

**Default Configuration:**
- Development: `http://localhost:8000`
- GraphQL Endpoint: `/graphql`
- CORS enabled for all origins

### Data Schema

The frontend uses the Lancer TTRPG reserve schema:

```javascript
{
  id: string,           // Unique identifier
  name: string,         // Display name
  type: enum,           // BONUS, RESOURCE, MECH, TACTICAL
  label: string,        // Category label
  description: string,  // HTML-compatible description
  bonuses: array,       // Optional bonus effects
  deployables: array,   // Optional deployable items
  actions: array,       // Optional activatable actions
  synergies: array,     // Optional synergy effects
  created_at: datetime,
  updated_at: datetime
}
```

## Technologies Used

- **Vue 3**: Progressive JavaScript framework
- **Composition API**: Vue's modern API for component logic
- **Pinia**: State management library for Vue
- **Bootstrap 5**: CSS framework for responsive design
- **Bootstrap Icons**: Icon library
- **Vite**: Build tool and development server
- **GraphQL**: API communication with backend
- **Native Fetch**: HTTP client for GraphQL requests

## Development Notes

- All components use the Composition API with `<script setup>` syntax
- Pinia provides centralized state management for reserves data
- Bootstrap 5 is loaded via CDN in the HTML template
- Components are organized in a logical folder structure
- GraphQL integration with error handling and loading states
- Form validation and error handling are implemented
- Responsive design works on all device sizes
- Environment-based configuration for different deployment environments

## Future Enhancements

- Add Vue Router for navigation
- Add state management (Pinia)
- Implement authentication
- Add reserve detail view with full schema display
- Add search and filtering capabilities
- Add unit tests
- Add GraphQL query optimization
