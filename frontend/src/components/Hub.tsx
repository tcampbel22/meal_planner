import React, { useState } from "react";
import { useAuth } from "../hooks/useAuth";
import { Link } from "react-router-dom";
import { AddRecipePopUp } from "./AddRecipePopUp";
import { SessionExpired } from "./Utils"


type hubCardProps = {
	title: string;
	onClick?: () => void;
	link?: string;
}




const HubCard:React.FC<hubCardProps> = ({ title, onClick, link }) => {
	return (
		<>
			{!link ? (
				<div className="flex flex-col items-center justify-center
								border border-2 shadow-sm rounded-sm
								md:w-60 md:h-70 w-60 h-20
								transition ease-in-out hover:scale-105
								bg-green-200 hover:cursor-pointer"
								onClick={onClick}
				>
					{title}
				</div>
			) : (
				<Link
					to={link}
					className="flex flex-col items-center justify-center
							border border-2 shadow-sm rounded-sm
							md:w-60 md:h-70 w-60 h-20
							transition ease-in-out hover:scale-105
							bg-green-200 hover:cursor-pointer"
							onClick={onClick}>
					{title}
				</Link>
			)}
		</>
	)
}

export const Hub:React.FC = () => {
	const [showAddRecipe, setShowAddRecipe] = useState<boolean>(false);
	const { isLoggedIn, user } = useAuth();
	const username = user?.username;

	return (
		<>
			{showAddRecipe && <AddRecipePopUp onClose={() => setShowAddRecipe(false)} />}
			{isLoggedIn ? (
				<div className="flex flex-col items-center justify-center h-full my-10 md:gap-y-10">
					<h1 className="text-2xl font-bold">Welcome {username}!</h1>
					<div className="flex md:flex-row flex-col items-center text-center gap-10 mt-20">
						<HubCard title="Add Recipe" onClick={() => setShowAddRecipe(true)}/>
						<HubCard title="Recipes" link="/recipes"/>
						<HubCard title="Generate mealplan" link="/mealplan"/>
						<HubCard title="Mealplan History"/>
					</div>
				</div>
			) : (
				<SessionExpired />
			)}
		</>
	)
}
