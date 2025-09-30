import React, { useState } from "react";
import GenericInput from "./Utils";
import { GenericButton } from "./ButtonUtils";

type AddRecipePopUpProps = {
	onClose: () => void;
  };

export const AddRecipePopUp:React.FC<AddRecipePopUpProps> = ({ onClose }) => {
	const [recipeName, setRecipeName] = useState<string>("")
	const [recipeUrl, setRecipeUrl] = useState<string>("")
	const [portionSize, setPortionSize] = useState<string>("")
	const [error, setError] = useState<string>("")
	const [info, setInfo] = useState<string | null>("")
	const [isSubmitting, setIsSubmitting] = useState<boolean>(false)

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault()
		setError("")
		setInfo("")

		setTimeout(() => {
			setError("")
			setInfo("")
			setRecipeName("")
			setRecipeUrl("")
			setPortionSize("")
			setIsSubmitting(false)
		}, 2000)

		if (!recipeName || !recipeUrl || !portionSize) {
			setError("Please fill in all fields")
			return
		}

		//Add add recipe endpoint here
		setIsSubmitting(true)
		setInfo("Recipe added successfully!")
		if (isSubmitting)
			setTimeout(() => onClose(), 2000)
	}

	return (
		<div className="fixed inset-0 flex justify-center bg-gray-950/95 items-center z-50">
			<div className="flex flex-col items-center pt-3 pb-10 border border-2 bg-violet-200 md:w-120">
			<div className="w-full flex justify-end items-end px-4">
          		<button onClick={onClose} className="text-4xl hover:scale-140 hover:cursor-pointer transition ease-in-out">&times;</button>
        	</div>
				<h2 className="text-2xl font-bold">Add Recipe</h2>
					<form
						className="flex flex-col justify-center gap-y-6 mt-10 w-full px-10"
						onSubmit={handleSubmit}
						>
						<GenericInput type="text" placeholder="Recipe name" value={recipeName} setValue={setRecipeName} />
						<GenericInput type="text" placeholder="Recipe URL" value={recipeUrl} setValue={setRecipeUrl} />
						<GenericInput type="text" placeholder="Portion size" value={portionSize} setValue={setPortionSize} />
						<GenericButton title={!isSubmitting ? "Submit!" : "Submitting..."} />
						{error && (<p className="text-red-600 font-semibold text-center">{error}</p>)}
						{info && (<p className="text-green-600 font-semibold text-center">{info}</p>)}
					</form>
			</div>

		</div>
	)
}
