import React from "react";
import { HeaderButton } from "./HeaderButton";

export const ServerError:React.FC = () => {
	return (
		<div className="flex flex-col items-center gap-y-10 my-auto">
			<h1 className="text-6xl font-bold">500</h1>
			<h2 className="text-3xl font-bold">Shiiiit... Something broke!</h2>
			<HeaderButton title="Back to homepage" link="/"/>
		</div>
	)
}
