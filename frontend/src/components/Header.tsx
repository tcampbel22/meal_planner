import React from "react";
import { HeaderButton } from "./HeaderButton";
import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";


export const Header:React.FC = () => {
	const { isLoggedIn, logout } = useAuth();
	return (
		<div className="flex md:flex-row flex-col md:justify-between items-center border-b-2 w-full bg-violet-200 gap-y-4 px-5 py-3">
			<Link to="/">
				<h1 className="text-4xl font-black">Mealwise</h1>
			</Link>

				{!isLoggedIn ? (
					<div className="flex md:flex-row flex-col gap-y-4 gap-x-4">
					<HeaderButton title="Login" link="/login"/>
					<HeaderButton title="Register" link="/register"/>
					</div>
				) :
				(
					<div className="flex md:flex-row text-center gap-y-4 gap-x-4">
					<HeaderButton title="Settings" link="/settings" />
					<HeaderButton title="Logout" link="/" action={logout}/>
					</div>
				)}
		</div>
	)
}
