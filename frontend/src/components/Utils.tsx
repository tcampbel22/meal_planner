import React from "react";

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

const GenericInput:React.FC<GenericInputProps> = ({
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

export default GenericInput
