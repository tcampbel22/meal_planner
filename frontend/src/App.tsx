import React from "react"
import { AppRoutes } from "./components/AppRoutes"
import { Footer } from "./components/Footer"
import { Header } from "./components/Header"

const App:React.FC = () => {

  return (
    <>
      <div className="flex flex-col font-mono bg-gray-100 dark:text-white dark:bg-gray-950 text-gray-900 text-xl w-full min-h-screen">
		<Header />
		<AppRoutes />
		<Footer />
	  </div>
    </>
  )
}

export default App
