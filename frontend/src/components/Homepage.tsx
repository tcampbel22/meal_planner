import React, { useState } from "react";
import { useAuth } from "../hooks/useAuth";
import { Hub } from "./Hub";

export const HomePage:React.FC = () => {
	const [showList, setShowList] = useState<boolean>(false)
	const { isLoggedIn } = useAuth();

 	const mealList = [
			"Red Curry with tofu",
			"Veg Tacos",
			"Beef Chili with rice",
			"Butter Paneer with naan",
			"Cauliflower pasta-bake",
		]

	const clicker = (showList: boolean) => {
		if (showList)
			setShowList(false)
		else
			setShowList(true)
	}
	return (
		<>
			{ !isLoggedIn ? (<div className="flex flex-col justify-center items-center text-xl gap-y-4 h-full">
				<h1 className="text-3xl mt-10">Meal planning made easy</h1>
				<button
					onClick={() => clicker(showList)}
					className="mt-20 mb-10 text-4xl border-4 p-8 bg-green-200 rounded-md hover:scale-110 hover:cursor-pointer transition ease-in-out">
						Generate
				</button>
				{!showList ? mealList.map(l => {
					return <ul key={l} className="text-lg/9">{l}</ul>
				}) : (<p></p>)}
			</div>) : (<Hub/>)}
		</>
	)
}
