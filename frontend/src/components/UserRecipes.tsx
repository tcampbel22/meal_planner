import { useEffect, useState } from "react";
import { useAuth } from "../hooks/useAuth";
import { BackButton, SessionExpired } from "./Utils";
import api from "../utils/api";
import axios, { AxiosError } from "axios";
import { ServerError } from "./ServerError";
import { Gear } from "@phosphor-icons/react";


const API_URL = import.meta.env.VITE_API_URL


type recipeProps = {
	recipeName: string;
	recipeUrl: string;
	portionSize: number;
	cuisine: string;
}

export const UserRecipes:React.FC = () => {
	const { isLoggedIn, user } = useAuth();
	const [error, setError] = useState<boolean>(false);
	const [recipes, setRecipes] = useState<recipeProps[]>([]);
	const headers = ["Recipe", "Url", "Cuisine", "Portions"]


	useEffect(() => {
		const fetchRecipes = async () => {

			try {
				const { data } = await api.get(`${API_URL}/recipes/me`)
				setRecipes(data)

			} catch (error: unknown) {
				if (axios.isAxiosError(error)) {
						const axiosError = error as AxiosError;
						if (axiosError.response?.status === 404) {
								console.error("User not found: Failed to fetch user");
							} else {
								console.error(`Failed to fetch recipes: ${axiosError.message}`);
							}
				}
				console.error(`Failed to fetch recipes: ${error}`)
				setError(true)
			}
		}
		if (isLoggedIn) fetchRecipes();
	}, [isLoggedIn])

	if (error) return <ServerError />
	if (!isLoggedIn || !user) return <SessionExpired />

	return (
		<div className="m-4">
				<BackButton link="/hub" />
				<div className="flex flex-col items-center mt-10 text-center">
				<h1 className="text-3xl font-bold">{user?.username}'s recipes</h1>
					<div className="grid grid-cols-5 gap-6 mt-20 p-4 border-b max-w-2xl md:min-w-6xl font-bold">

							{headers.map((h, i) => {
								return <h2 key={i}>{h}</h2>
							})}
					</div>
					<div className="max-h-75 md:max-h-150 overflow-auto">
						{recipes.map((r, idx) => {
							return (
								<div key={idx} className="grid grid-cols-5 border-b p-4 max-w-2xl md:min-w-6xl">
									<div className="text-left truncate">{r.recipeName}</div>
                                    <a href={r.recipeUrl} className="truncate hover:underline" target="_blank" rel="noopener noreferrer">
										{r.recipeUrl[4] == ':' ? r.recipeUrl.slice(7) : r.recipeUrl.slice(8)}</a>
                                    <div className="flex justify-center">{r.cuisine}</div>
                                    <div className="flex justify-center">{r.portionSize}</div>
                                    <div className="flex justify-center hover:scale-110 hover:cursor-pointer"><Gear size={32} /></div>
								</div>
								)
							})}
					</div>
				</div>
		</div>
	)
}
