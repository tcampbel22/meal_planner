import React from "react";
import { Route, Routes } from "react-router-dom";
import { HomePage } from "./Homepage";
import { Login } from "./Login";
import { NotFound } from "./NotFound";
import { Register } from "./Register";
import { Hub } from "./Hub";
import { UserRecipes } from "./UserRecipes";
import { MealPlan } from "./MealPlan";

export const AppRoutes:React.FC = () => {
	return (
		<Routes>
			<Route path="/" element={<HomePage />}/>
			<Route path="/login" element={<Login />} />
			<Route path="/register" element={<Register />} />
			<Route path="/hub" element={<Hub />} />
			<Route path="/recipes" element={<UserRecipes />} />
			<Route path="/mealplan" element={<MealPlan />} />
			<Route path="*" element={<NotFound />} />
		</Routes>
	)
}
