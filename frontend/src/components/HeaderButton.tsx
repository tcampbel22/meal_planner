import React from "react";
import { Link } from "react-router-dom";

type HeaderButtonProps = {
	title: string,
	link: string
}

export const HeaderButton:React.FC<HeaderButtonProps> = ({ title, link }) => {
	return (
		<Link
			className="border-2 border-bg-black rounded-sm px-4 py-3
						hover:scale-110 hover:cursor-pointer hover:bg-violet-400 transition ease-in-out"
			to={link}>
			{title}
		</Link>
	)
}
