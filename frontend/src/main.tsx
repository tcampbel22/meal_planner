import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import { HashRouter } from 'react-router-dom'
import axios from 'axios'
import { AuthProvider } from './components/Auth.tsx'

axios.defaults.withCredentials = true;

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <HashRouter>
	  <AuthProvider>
	    <App />
	  </AuthProvider>
	</HashRouter>
  </StrictMode>,
)
