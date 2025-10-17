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

### Installation

1. Navigate to the app directory:
   ```bash
   cd app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

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
- Integrate with backend API
- Add state management (Pinia)
- Implement authentication
- Add more interactive features
- Add unit tests
