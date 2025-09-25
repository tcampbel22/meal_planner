import React from "react";
// import { Link } from "react-router-dom";


type GenericButtonProps = {
	title: string;
	width?: number;
	height?: number;
}

export const GenericButton:React.FC<GenericButtonProps> = ({ title }) => {
	return (
		<button
			className="border-1 px-20 rounded-sm text-center py-3 hover:bg-violet-400 hover:scale-105 transition ease-in-out"
		>
			{title}
		</button>
	)
}
