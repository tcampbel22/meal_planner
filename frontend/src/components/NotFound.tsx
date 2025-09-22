import React from "react";
import { HeaderButton } from "./HeaderButton";

export const NotFound:React.FC = () => {
	return (
		<div className="flex flex-col items-center gap-y-10 my-auto">
			<h1 className="text-6xl font-bold">404</h1>
			<h2 className="text-3xl font-bold">Looks like you're lost!</h2>
			<HeaderButton title="Back to homepage" link="/"/>
		</div>
	)
}
