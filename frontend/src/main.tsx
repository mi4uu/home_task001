import React from 'react'
import { BrowserRouter } from "react-router-dom"
import { QueryClientProvider } from 'react-query'
import ReactDOM from 'react-dom/client'
import App from './App'
import './css/normalize.css'
import './css/style.css'

import { queryClient } from './store/store'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    </BrowserRouter>
  </React.StrictMode>
)
