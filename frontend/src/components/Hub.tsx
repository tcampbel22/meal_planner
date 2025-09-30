import React, { useState } from "react";
import { useAuth } from "../hooks/useAuth";
import { Link } from "react-router-dom";
import { AddRecipePopUp } from "./AddRecipePopUp";

type hubCardProps = {
	title: string
	onClick?: () => void;
}


const HubCard:React.FC<hubCardProps> = ({ title, onClick }) => {
	return (
		<div className="flex flex-col items-center justify-center
						border border-2 shadow-sm rounded-sm
						md:w-60 md:h-70 w-60 h-20
						transition ease-in-out hover:scale-105
						bg-green-200 hover:cursor-pointer"
			onClick={onClick}>
			{title}
		</div>
	)

}

export const Hub:React.FC = () => {
	const [showAddRecipe, setShowAddRecipe] = useState<boolean>(false);
	const { isLoggedIn, user } = useAuth();
	const username = user?.username

	return (
		<>
			{showAddRecipe && <AddRecipePopUp onClose={() => setShowAddRecipe(false)} />}
			{isLoggedIn ? (
				<div className="flex flex-col items-center justify-center h-full my-10 md:gap-y-10">
					<h1 className="text-2xl font-bold">Welcome {username}!</h1>
					<div className="flex md:flex-row flex-col items-center text-center gap-10 mt-20">
						<HubCard title="Add Recipe" onClick={() => setShowAddRecipe(true)}/>
						<HubCard title="Recipes"/>
						<HubCard title="Generate mealplan"/>
						<HubCard title="Mealplan History"/>
					</div>
				</div>
			) : (
				<div className="flex flex-col gap-y-10 justify-center items-center my-10">
					<h1 className="text-2xl font-bold">Oho! Looks like your session expired</h1>
					<Link
						to={"/"}
						className="p-4 border border-2 bg-violet-200 transition ease-in-out hover:scale-110">
						Back to home
					</Link>
				</div>
			)}
		</>
	)
}
