import React from "react";
import { HeaderButton } from "./HeaderButton";
import { Link } from "react-router-dom";

export const Header:React.FC = () => {
	return (
		<div className="flex md:flex-row flex-col md:justify-between items-center border-b-2 w-full bg-violet-200 px-5 py-3">
			<Link to="/">
				<h1 className="text-4xl font-black">Mealwise</h1>
			</Link>

			<div className="flex gap-y-4 gap-x-4">
				<HeaderButton title="Login" link="/login"/>
				<HeaderButton title="Register" link="/register"/>
			</div>
		</div>
	)
}
