import React, { useState } from "react";
import { GenericInput } from "./Utils";
import { GenericButton } from "./ButtonUtils";
import api from "../utils/api";
import axios, {AxiosError } from "axios";

type AddRecipePopUpProps = {
	onClose: () => void;
  };

export const AddRecipePopUp:React.FC<AddRecipePopUpProps> = ({ onClose }) => {
	const [recipeName, setRecipeName] = useState<string>("")
	const [recipeUrl, setRecipeUrl] = useState<string>("http://")
	const [portionSize, setPortionSize] = useState<number | string>(2)
	const [cuisine, setCuisine] = useState<string>("")
	const [error, setError] = useState<string | null>(null)
	const [info, setInfo] = useState<string | null>(null)
	const [isSubmitting, setIsSubmitting] = useState<boolean>(false)


	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault()
		setError(null)
		setInfo(null)
		setIsSubmitting(true)

		if (!recipeName || !portionSize) {
			setError("Please fill in all fields")
			setIsSubmitting(false)
			return
		}
		const payload = {
			recipeName,
			recipeUrl,
			portionSize,
			cuisine
		}
		try {
			console.log(payload)
			const response = await api.post(`/recipes`, payload)
			console.log(response)
			setInfo("Recipe added successfully!")
			setTimeout(() => {
				onClose()
			}, 2000)

		} catch (error: unknown){
			if (axios.isAxiosError(error)) {
				const axiosError = error as AxiosError;
				if (axiosError.response?.status == 409)
					setError("Recipe already exists")
				else if (axiosError.response?.status == 422)
					setError("Invalid recipe format")
				else
					setError("Failed to add recipe, please try again")
			} else {
				setError("Failed to add recipe")
			}
			console.error(`Failed to add recipe: ${error}`)
		} finally {
            setTimeout(() => {
                setError(null)
                setInfo(null)
                if (!error) {
                    setRecipeName("")
                    setRecipeUrl("http://")
                    setPortionSize(2)
                    setCuisine("")
                }
                setIsSubmitting(false)
            }, 2000)
        }

	}

	return (
		<div className="fixed inset-0 flex justify-center bg-gray-950/95 items-center z-50">
			<div className="flex flex-col items-center pt-3 pb-10 border border-2 bg-violet-200 md:w-120">
			<div className="w-full flex justify-end items-end px-4">
          		<button onClick={onClose} className="text-4xl hover:scale-140 hover:cursor-pointer transition ease-in-out">&times;</button>
        	</div>
				<h2 className="text-2xl font-bold">Add Recipe</h2>
					<form
						className="flex flex-col justify-center gap-y-6 w-full px-10 mt-10"
						onSubmit={handleSubmit}
						>
						<GenericInput type="text" placeholder="Spaghetti..." label="Recipe name*" value={recipeName} setValue={setRecipeName} required />
						<GenericInput type="url" placeholder="Recipe URL" label="URL" value={recipeUrl} setValue={setRecipeUrl} />
						<GenericInput type="number" placeholder="Portion size" label="Portions*" value={portionSize} setValue={setPortionSize} required/>
						<GenericInput type="text" placeholder="Italian..." label="Cuisine" value={cuisine} setValue={setCuisine} />
						<GenericButton title={!isSubmitting ? "Submit!" : "Submitting..."} />
						{error && (<p className="text-red-600 font-semibold text-center">{error}</p>)}
						{info && (<p className="text-green-600 font-semibold text-center">{info}</p>)}
					</form>
			</div>

		</div>
	)
}
