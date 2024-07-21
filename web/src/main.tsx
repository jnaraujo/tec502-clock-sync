import React from "react"
import ReactDOM from "react-dom/client"
import "./index.css"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { Toaster } from "react-hot-toast"
import { HomePage } from "./pages/home"

const queryClient = new QueryClient()

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <HomePage />
      <Toaster />
    </QueryClientProvider>
  </React.StrictMode>,
)
