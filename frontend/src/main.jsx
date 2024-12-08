import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { UserProvider } from './userContext.jsx'
import { BrowserRouter } from 'react-router-dom'

const root = createRoot(document.getElementById('root'));
root.render(
    <StrictMode>
      <BrowserRouter>
        <UserProvider>
            <App />
        </UserProvider>
      </BrowserRouter>
    </StrictMode>
);