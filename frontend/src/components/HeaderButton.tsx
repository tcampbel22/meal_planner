import React from "react";
import { Link } from "react-router-dom";

type HeaderButtonProps = {
	title: string,
	link: string,
	action?: () => void
}

export const HeaderButton:React.FC<HeaderButtonProps> = ({ title, link, action }) => {
	const handleClick = (e: React.MouseEvent) => {
        if (action) {
            e.preventDefault();
            action();
        }
    };
	return (
		<Link
			className="border-2 border-bg-black rounded-sm px-4 py-3
						hover:scale-110 hover:cursor-pointer hover:bg-violet-400 transition ease-in-out"
			onClick={handleClick}
			to={link}
			>
			{title}
		</Link>
	)
}
