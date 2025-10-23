import React, { useEffect, useState } from "react";
import { BackButton, SessionExpired } from "./Utils";
import { useAuth } from "../hooks/useAuth";

type mealPlanProps = {
	meal: string;
}

export const MealPlan:React.FC = () => {
	const { isLoggedIn } = useAuth();
	const [mealPlan, setMealPlan] = useState<mealPlanProps[]>([]);
	const plan = [
		{ "meal": "eat shit" },
		{ "meal": "eat more shit" },
		{ "meal": "eat slightly less shit" },
	]
	useEffect(() => {
		console.log("Here")
		setMealPlan(plan)
		// Call mealplan endpoint here
	}, [])
	if (!isLoggedIn) return <SessionExpired />
	return (
		<div className="m-4">
			<BackButton link="/hub" />
			<h1 className="flex flex-col text-center items-center font-bold">Meal plan</h1>
			<div className="flex flex-col items-center jusitfy-center gap-y-6 mt-6">
				{mealPlan.map((r, i) => {
					return <p key={i} className="py-1">Day {i + 1}: {r.meal}</p>
				})}
			</div>
		</div>
	)
}
