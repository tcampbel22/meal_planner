import React from "react";
import { Link } from "react-router-dom";
import { ArrowSquareLeftIcon } from '@phosphor-icons/react'


type GenericInputProps = {
	type: string;
	placeholder: string;
	value: string | number;
	minLength?: number;
	maxLength?: number;
	required?: boolean;
	label?: string;
	setValue: (value: string) => void;
}

type BackButtonProps = {
	link: string;
}

export const GenericInput:React.FC<GenericInputProps> = ({
	type,
	placeholder,
	value,
	minLength = 3,
	maxLength = 100,
	label,
	required = false,
	setValue }) => {
	return (
		<div className="flex flex-col items-center text-lg">
			<label>{label}</label>
			<input
				className="text-lg border border-1 bg-violet-100 rounded-sm pl-2 py-3 w-full"
				type={type}
				placeholder={placeholder}
				value={value}
				minLength={minLength}
				maxLength={maxLength}
				required={required}
				onChange={(e) => setValue(e.target.value)}
				/>
		</div>
	)
}

export const SessionExpired:React.FC = () => {
	return (
		<div className="flex flex-col gap-y-10 justify-center items-center my-10">
			<h1 className="text-2xl font-bold">Oho! Looks like your session expired</h1>
				<Link
					to={"/"}
					className="p-4 border border-2 bg-violet-200 transition ease-in-out hover:scale-110">
					Back to home
				</Link>
		</div>
	)
}

export const BackButton:React.FC<BackButtonProps> = ( { link } ) => {
	return (
		<Link
			to={link}
			className={"transform hover:scale-110 transition-all duration-300 ease-in-out"}>
			<ArrowSquareLeftIcon size={64} color={'#000000'}/>
		</Link>	)
}
