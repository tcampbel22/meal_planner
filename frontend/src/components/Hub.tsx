import React from "react";
import { useAuth } from "./Auth";

export const Hub:React.FC = () => {
	const { isLoggedIn } = useAuth();
	return (
		<div>
			{isLoggedIn ? (
				<h1 className="flex flex-col items-center">Welcome!</h1>
			) : (
				<h1 className="flex flex-col items-center">Please login</h1>
			)}
		</div>
	)
}
