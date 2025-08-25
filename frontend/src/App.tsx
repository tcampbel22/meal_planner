import React from "react"
import { HomePage } from "./components/Homepage"

const App:React.FC = () => {

  return (
    <>
      <div className="font-mono dark:text-white dark:bg-gray-950 text-gray-900 text-xl w-full h-full">
		<HomePage />
	  </div>
    </>
  )
}

export default App
